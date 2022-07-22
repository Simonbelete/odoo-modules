odoo.define('esign.sign_builder', function (require) {
    'use strict';

    var core = require('web.core');
    var QWeb = core.qweb;
    var AbstractAction = require('web.AbstractAction');

    var sign_builder = AbstractAction.extend({
        start: function () {
           
        }
    });

    core.action_registry.add('sign_builder_registry', sign_builder);
    return sign_builder;
});