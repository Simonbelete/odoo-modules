odoo.define('esign.sign_builder', function (require) {
    'use strict';

    var core = require('web.core');
    var QWeb = core.qweb;
    var AbstractAction = require('web.AbstractAction');

    var sign_builder = AbstractAction.extend({
        start: function () {
            this.renderBody();
        },
        setupGlobalVars: function () {
            this.$container = this.$('#container')[0];
        },
        renderBody: function () {
            this.$('.o_content').append(QWeb.render('sign_builder_body', {Widget: this}))
            this.$('.o_content').css({'overflow': 'hidden'})
        },
    });

    core.action_registry.add('sign_builder_registry', sign_builder);
    return sign_builder;
});