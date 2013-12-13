var ps = require('promise-streams');
var request = require('request');
var split = require('split');
var Promise = require('bluebird');
var ini = require('ini');
var fs = require('fs');
var args = require('optimist').argv;
var parseDosie = require('./parse-dosie');

Promise.promisifyAll(request);
require('http').globalAgent.maxSockets = 1024;

var config = ini.parse(fs.readFileSync(args.config, 'utf8'));

var totalProcessed = 0;

request(couchUrl('_all_docs'))
    .pipe(split())
    .pipe(ps.through(parseCouchJson)) 
    .pipe(ps.map({limit: 256}, processDocument))
    .wait()

function couchUrl(req) {
    return config.database.url + '/' + req;
}

function parseCouchJson(line) {
    if (!line) return
    // clean comma
    if (line[line.length - 1] == ',')
        line = line.substr(0, line.length - 1)
    // parse and push
    try { return this.push(JSON.parse(line)); }
    catch (e) { } // skip
}

function notFoundError(e) {
    return e.message.indexOf(404) >= 0;
}


var stats = {skipped: 0, parsed: 0, notfound: 0, t: Date.now()}
function processDocument(doc) {
    return fetchDocument(doc.id).then(function(doc) {
        if (doc.state == 'parsed-spion') 
            return ++stats.skipped;
        return parseDosie(couchUrl(doc._id + '/dosie.html'), config.selectors)
        .then(function(dosieInfo) {
            doc.state = 'parsed-spion';
            ++stats.parsed;
            //console.log('Updating', doc.link);            
            return updateDocument(doc._id, merge(doc, dosieInfo));
        }).catch(notFoundError, function() {
            ++stats.notfound;
            //console.log("Not found", doc.link, '(' + doc.state + ')');
        })
    }).then(function() {
        ++totalProcessed;
        if (totalProcessed % 50 === 0) {
            stats.t = ((Date.now() - stats.t) / 1000).toFixed(1);
            stats.spd = ((stats.skipped 
                         + stats.parsed 
                         + stats.notfound) / stats.t).toFixed(1)
            console.log("Processed", totalProcessed, stats);
            stats = {skipped: 0, parsed: 0, notfound: 0, t: Date.now()}
        }
    });

}

function fetchDocument(id) {
    return request.getAsync(couchUrl(id))
    .spread(function(res, body) { 
        return JSON.parse(body);
    });
}

function updateDocument(id, content) {
    var url = couchUrl(id);
    request.putAsync({
        url: url, 
        headers: {
            referer: url,
            'content-type': 'application/json'
        },
        auth: config.database,
        body: JSON.stringify(content)
    }).spread(function(res, body) {
        if (res.statusCode >= 400)
            throw new Error('HTTP Response ' + res.statusCode + ' ' 
                            + url + body);
        return body;
    });
}

function merge(obj, extra) {
    var merged = {};
    for (var key in obj)
        merged[key] = obj[key];
    for (var key in extra)
        merged[key] = extra[key];
    return merged;
}

