/*
 * This casperjs script will open the web site of public procurements done
 * by Macedonian government and public companies, crawl to the specified page
 * in the list and extract the links to all the actual procurements.
 *
 * We must use casperjs because the site uses ASP and its stupid ajax pagination.
 *
 * Further processing of the links will be done with other tools.
 *
 */


var URL = "https://e-nabavki.gov.mk/PublicAccess/NotificationForACPP/default.aspx?Level=3";
var casper = require('casper').create();

var pageNum = casper.cli.options['page'] || 1;
pageNum = pageNum - 1; // the select is 0 based, but --page is 1 based
var links = [];

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
    this.echo(JSON.stringify({links:links, page:pageNum+1, length:links.length}, undefined, 4)).exit();
});
