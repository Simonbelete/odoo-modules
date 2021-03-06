odoo.define('manpower_report', function (require) {
  'use strict';

var core = require('web.core');
var QWeb = core.qweb;
var AbstractAction = require('web.AbstractAction');

var manpower_report = AbstractAction.extend({
  init: function(parent, context) {
    this._super(parent, context)
    this.date_from = ''
    this.date_to = ''
  },
  get_html: async function() {
    console.log(this.date_from)
    console.log(this.date_to)
    const html = await this._rpc({
      args: [this.date_from, this.date_to],
      model: 'report.stadia.manpower_report',
      method: 'get_html'
    })
    this.html = html

  },
  set_html: function() {
    var self = this;
    self.$('.o_content').append(QWeb.render('o_control_panel', {widget: self}))
    self.$('.o_cp_bottom_left').append(QWeb.render('manpower_report_print_button', {widget: self}))
    var form = self.$('.o_cp_top_right').append(QWeb.render('manpower_report_form', {widget: self}))
    // Bind Actions
    form.find('.man_from_date').on('change',this._onchageFromDate.bind(this)).change()
    form.find('.man_to_date').on('change',this._onchageFromTo.bind(this)).change()
    self.$('.o_content').append(this.html)
  },
  start: async function() {
    await this.get_html()
    this.set_html()
  },
  _onchageFromDate: function(ev) {
    var date = $(ev.currentTarget).val()
    if(date){
      this.date_from = date;
      this._reload();
    }
  },
  _onchageFromTo: function(ev) {
    var date = $(ev.currentTarget).val()
    if(date){
      this.date_to = date;
      this._reload();
    }
  },
  _reload: async function() {
    await this.get_html()
    self.$('.man_report_tables').replaceWith(this.html)
  },
})

core.action_registry.add('stadia_manpower_reg', manpower_report);
return manpower_report;

})