var URL = "https://e-nabavki.gov.mk/PublicAccess/NotificationForACPP/default.aspx?Level=3";
var links = [];
var casper = require('casper').create();

var pageSelectorName = "ctl00$ctl00$cphGlobal$cphPublicAccess$ucNotificationForACPP$gvNotifications$ctl13$ddlPageSelector";
var pageNum = 9;
var paginationPageNumSelector = ".PagerStyle > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > span:nth-child(1)";


casper.start(URL, function() {
   // select page
   var form = {};
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
   return this.evaluate(function() {
      var pag = document.querySelector('.PagerStyle');
      console.log(pag.textContent);
      return pag.textContent.indexOf('до 100 од') != -1;
   });
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
       var x = [];
       x = getLinks('.RowStyle a[href]');
       return x.concat(getLinks('.AltRowStyle a[href]'));
    });
});

casper.run(function() {
    // echo results in some pretty fashion
    this.echo(JSON.stringify({links:links}, undefined, 4).exit();
});