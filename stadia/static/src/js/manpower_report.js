odoo.define('manpower_report', function (require) {
  'use strict';

var core = require('web.core');
var QWeb = core.qweb;
var AbstractAction = require('web.AbstractAction');

var manpower_report = AbstractAction.extend({
  get_html: async function() {
    const html = await this._rpc({
      // args: [this.given_context],
      model: 'report.stadia.manpower_report',
      method: 'get_html'
    })
    this.html = html
  },
  set_html: function() {
    var self = this;
    self.$('.o_content').append(QWeb.render('o_control_panel', {widget: self}))
    self.$('.o_cp_bottom_left').append(QWeb.render('manpower_report_print_button', {widget: self}))
    self.$('.o_cp_top_right').append(QWeb.render('manpower_report_form', {widget: self}))
    self.$('.o_content').append(this.html)
  },
  start: async function() {
    await this.get_html()
    this.set_html()
  }
})

core.action_registry.add('stadia_manpower_reg', manpower_report);
return manpower_report;

})