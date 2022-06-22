odoo.define('asset_report', function (require) {
'use strict';

var core = require('web.core');
var QWeb = core.qweb;
var stock_report_generic = require('stock.stock_report_generic');


var AssetReport = stock_report_generic.extend({
  get_html: function() {
    var self = this;
    var args = [
      this.given_context.date
    ]
    return this._rpc({
      model: 'report.stadia.asset_report',
      method: 'get_html',
      args: args,
      context: this.given_context
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
    this.$buttonPrint = $(QWeb.render('asset_print_report_button'))
    this.$buttonPrint.find('.s_asset_report_print').on('click', this._onClickPrint.bind(this));
    this.$searchView = $(QWeb.render('asset_search_report'));
    this.$searchView.find('.s_asset_report_date').on('change', this._onChangeDate.bind(this)).change()
  },
  // Add contenet to odoo header
  update_cp: function() {
    var status = {
      cp_content: {
        $buttons: this.$buttonPrint,
        $searchview: this.$searchView
      }
    }
    return this.updateControlPanel(status);
  },
  _onChangeDate: function(ev) {
    var date = $(ev.currentTarget).val()
    console.log(date)
    if(date){
      this.given_context.date = date;
      this._reload()
    }
  },
  _reload: function() {
    var self = this;
    return this.get_html().then(function () {
      self.$('.o_content').html(self.data.lines);
    })
  },
  _onClickPrint: function() {
    var context = "{'date': '" + this.given_context.date + "'}"
    var action = {
      'type': 'ir.actions.report',
      'model': 'stadia.asset',
      'report_type': 'xlsx',
      'report_name': 'stadia.asset_report?docids=0',
      'report_file': 'abd',
      'context': context
    };
    return this.do_action(action).then(function (){
        // framework.unblockUI();
    });
  }
})

core.action_registry.add('stadia_asset_reg', AssetReport);
return AssetReport;

})