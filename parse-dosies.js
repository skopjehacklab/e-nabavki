var request = require('request');
var Promise = require('bluebird');
var cheerio = require('cheerio');
var args = require('optimist').argv;
var fs = require('fs');
var ini = require('ini');

Promise.promisifyAll(request);

var config = ini.parse(fs.readFileSync(args.config, 'utf8'));

extractData(args.url, config.selectors)
    .then(function outputResult(res) {
        console.log(res);
    });

function extractData(url, fields) {
    return loadData(url)
        .then(function(body) { 
            return extractFields(body, fields);
        })
}

function loadData(url) {
    return request.getAsync(url)
        .spread(function getBody(res, body) {
            return body;
        })
}

function extractFields(html, selectors) {
    var $ = cheerio.load(html)
    var results = {};
    for (var selector in selectors) {
        var fieldName = selectors[selector];
        results[fieldName] = $('#' + selector).text();
    }
    return results;
}

