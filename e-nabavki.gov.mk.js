var URL = "https://e-nabavki.gov.mk/PublicAccess/NotificationForACPP/default.aspx?Level=3";
var links = [];
var casper = require('casper').create();

var pageNum = casper.cli.options['page'] || 0;

casper.on('remote.message', function(message) {
    console.log(message);
});

casper.start(URL, function() {
   // select page
   var form = {};
   var pageSelectorName = "ctl00$ctl00$cphGlobal$cphPublicAccess$ucNotificationForACPP$gvNotifications$ctl13$ddlPageSelector";
   form[pageSelectorName] = pageNum;
   this.fill('form', form);
});

/*
casper.wait(8000, function() {
   this.capture('out.png');
   this.echo('screenshot made');
});
*/

casper.waitFor(function check() {
   // wait for ajax pagination
   return this.evaluate(function(pageNum) {
      var pag = document.querySelector('.PagerStyle');
      return pag.textContent.indexOf('до ' + (pageNum + 1) * 10 + ' од') != -1;
   }, pageNum);
}, undefined, undefined, 15000);

casper.then(function() {
   // aggregate all links
    links = this.evaluate(function () {
       function getLinks(q) {
          var elements = document.querySelectorAll(q);
          return Array.prototype.map.call(elements, function(e) {
             return e.getAttribute('href');
          });
       }
       var all_links = [];
       all_links = getLinks('.RowStyle td:nth-child(1) a[href]');
       all_links = all_links.concat(getLinks('.AltRowStyle td:nth-child(1) a[href]'));
       return all_links.map(function(el) {
         return el.replace('..', 'https://e-nabavki.gov.mk/PublicAccess');
       })
    });
});

casper.run(function() {
    // echo results in some pretty fashion
    this.echo(JSON.stringify({links:links, page:pageNum, length:links.length}, undefined, 4)).exit();
});