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
		
		// pdfjsLib.GlobalWorkerOptions.workerSrc =
		// 'esign/static/src/libs/pdfjs/pdf.worker.js';
		var url = 'helloworld.pdf';
		// loadingTask.promise.then(function(pdf) {
		// // you can now use *pdf* here
		// });

		const loadingTask = pdfjsLib.getDocument(url);
  (async () => {
    const pdf = await loadingTask.promise;
    //
    // Fetch the first page
    //
    const page = await pdf.getPage(1);
    const scale = 1.5;
    const viewport = page.getViewport({ scale });
    // Support HiDPI-screens.
    const outputScale = window.devicePixelRatio || 1;

    //
    // Prepare canvas using PDF page dimensions
    //
    const canvas = document.getElementById("the-canvas");
    const context = canvas.getContext("2d");

    canvas.width = Math.floor(viewport.width * outputScale);
    canvas.height = Math.floor(viewport.height * outputScale);
    canvas.style.width = Math.floor(viewport.width) + "px";
    canvas.style.height = Math.floor(viewport.height) + "px";

    const transform = outputScale !== 1 
      ? [outputScale, 0, 0, outputScale, 0, 0] 
      : null;

    //
    // Render PDF page into canvas context
    //
    const renderContext = {
      canvasContext: context,
      transform,
      viewport,
    };
    page.render(renderContext);
  })();
	}
});

core.action_registry.add('esign_pdf_edit_reg', pdf_edit);

return pdf_edit;

});