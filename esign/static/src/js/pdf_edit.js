odoo.define('esign.pdf_edit', function (require) {
'use strict';

var core = require('web.core');
var QWeb = core.qweb;
var AbstractAction = require('web.AbstractAction');

var pdf_edit = AbstractAction.extend({
	start: function () {
		var self = this;
		self.$('.o_content').append(QWeb.render('esing_body', {widget: self}))
		console.log('Started')
		
		var url = 'https://raw.githubusercontent.com/mozilla/pdf.js/ba2edeae/examples/learning/helloworld.pdf';

    var loadingTask = pdfjsLib.getDocument('esign/static/src/js/helloworld.pdf');
    loadingTask.promise.then(function(pdf) {
      // you can now use *pdf* here
    });

		// End

	}
});

core.action_registry.add('esign_pdf_edit_reg', pdf_edit);

return pdf_edit;

});