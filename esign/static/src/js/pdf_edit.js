odoo.define('esign.pdf_edit', function (require) {
'use strict';

var core = require('web.core');
var QWeb = core.qweb;
var AbstractAction = require('web.AbstractAction');
// const { jsPDF } = require("jspdf");

var pdf_edit = AbstractAction.extend({
	start: function () {
		var self = this;
		self.$('.o_content').append(QWeb.render('esing_body', {widget: self}))
		console.log('Started')
		
		var url = 'https://raw.githubusercontent.com/mozilla/pdf.js/ba2edeae/examples/learning/helloworld.pdf';


    const doc = new jspdf.jsPDF();

    doc.text("Hello world!", 10, 10);
    doc.text("ListBox:", 10, 115);
    var listbox = new jspdf.AcroForm.ListBox();
    listbox.edit = false;
    listbox.fieldName = "ChoiceField2";
    listbox.topIndex = 2;
    listbox.Rect = [50, 110, 30, 10];
    listbox.setOptions(["c", "a", "d", "f", "b", "s"]);
    listbox.value = "s";
    doc.addField(listbox);

    url = doc.output('bloburi')

    var loadingTask = pdfjsLib.getDocument(url);
    loadingTask.promise.then(function(pdf) {

      var pageNumber = 1;
      pdf.getPage(pageNumber).then(function(page) {
        var scale = 1.5;
        var viewport = page.getViewport({scale: scale});

        var canvas = document.getElementById('pdf-js-viewer');
        var context = canvas.getContext('2d');
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        // Render PDF page into canvas context
        var renderContext = {
          canvasContext: context,
          viewport: viewport
        };
        var renderTask = page.render(renderContext);
        renderTask.promise.then(function () {
          console.log('Page rendered');
        });
      })
    });

		// End

	}
});

core.action_registry.add('esign_pdf_edit_reg', pdf_edit);

return pdf_edit;

});