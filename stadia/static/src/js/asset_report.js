odoo.define('asset_report', function (require) {
'use strict';

var core = require('web.core');
var QWeb = core.qweb;
var stock_report_generic = require('stock.stock_report_generic');


var AssetReport = stock_report_generic.extend({
  get_html: function() {
    var self = this;
    return this._rpc({
      model: 'report.stadia.asset_report',
      method: 'get_html'
    }).then(function (result) {
      self.data = result
    })
  },
  set_html: function() {
    var self = this;
    return this._super().then(function() {
      self.$('.o_content').html(self.data.lines);
      self.renderSearch()
      self.update_cp();
    })
  },
  renderSearch: function() {
    this.$searchView = $(QWeb.render('asset_search_report'))
  },
  update_cp: function() {
    var status = {
      cp_content: {
        $searchview: this.$searchView
      }
    }
    return this.updateControlPanel(status);
  }
})

core.action_registry.add('stadia_asset_reg', AssetReport);
return AssetReport;

})