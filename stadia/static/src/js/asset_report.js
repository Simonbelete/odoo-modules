odoo.define('asset_report', function (require) {
'use strict';

var core = require('web.core');
var AbstractAction = require('web.AbstractAction');
var QWeb = core.qweb;
var stock_report_generic = require('stock.stock_report_generic');

var AssetReport = stock_report_generic.extend({
  start: function() {
    
  }
})

core.action_registry.add('stadia_asset_reg', AssetReport);
return AssetReport;

})