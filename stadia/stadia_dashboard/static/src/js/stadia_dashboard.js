odoo.define('stadia_dashboard.custom_dashboard', function (require) {
'use strict';

var core = require('web.core');
var AbstractAction = require('web.AbstractAction');
var QWeb = core.qweb;

var Dashboard = AbstractAction.extend({
  template: 'eg_template',
  init: function(parent, context) {
    this._super(parent, context)
    console.log("Hello world")
  },
  start: function() {
    var self = this;
    self.$('.sta_con').append(QWeb.render('s_dashboard', {widget: self}))
    return this._super().then(function() {
      self.$('.sta_con').append(QWeb.render('s_dashboard', {widget: self}))
  });
  }
})

core.action_registry.add('stadia_dashboard_reg', Dashboard);
return Dashboard;

});