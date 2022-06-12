odoo.define('asset_report', function (require) {
'use strict';

var core = require('web.core');
var QWeb = core.qweb;
var stock_report_generic = require('stock.stock_report_generic');


var AssetReport = stock_report_generic.extend({
  // template: 'eg_template',
  start: function() {
    var self = this;
    self.$('.sta_con').append(QWeb.render('s_dashboard', {widget: self}))
    return this._super().then(function() {
      self.$('.sta_con').append(QWeb.render('s_dashboard', {widget: self}))
    });
  }
})

core.action_registry.add('stadia_asset_reg', AssetReport);
return AssetReport;

})