odoo.define('esign.pdf_edit', function (require) {
'use strict';

var core = require('web.core');
var QWeb = core.qweb;
var AbstractAction = require('web.AbstractAction');

var pdf_edit = AbstractAction.extend({
	start: function () {
		console.log('Started')
	}
});

core.action_registry.add('esign_pdf_edit_reg', pdf_edit);

return pdf_edit;

});