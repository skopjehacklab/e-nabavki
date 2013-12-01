var URL = "https://e-nabavki.gov.mk/PublicAccess/NotificationForACPP/default.aspx?Level=3";
var links = [];
var casper = require('casper').create();



casper.start(URL, function() {
    // aggregate results for the 'casperjs' search
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
    this.echo(links.length + ' links found:');
    this.echo(' - ' + links.join('\n - ')).exit();
});
