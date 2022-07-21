odoo.define('esing.frontend', function (require) {
  'use strict';

  var core = require('web.core');
  var QWeb = core.qweb;
  var AbstractAction = require('web.AbstractAction');
  var pdfBackedn = require('esign.pdf_edit');

  var pdf_rontend = pdfBackedn.extend({
    randomFunc: function() {
      console.lgo('random function called')

      // var url = 'esign/static/src/js/helloworld.pdf';

      // var loadingTask = pdfjsLib.getDocument(url);
      // loadingTask.promise.then(function(pdf) {
      //   var pageNumber = 1;
      //   pdf.getPage(pageNumber).then(function(page) {
      //     console.log('Page loaded');
          
      //     var scale = 1.5;
      //     var viewport = page.getViewport({scale: scale});

      //     // Prepare canvas using PDF page dimensions
      //     var canvas = document.getElementById('pdf_canvas');
      //     var context = canvas.getContext('2d');
      //     canvas.height = viewport.height;
      //     canvas.width = viewport.width;

      //     // Render PDF page into canvas context
      //     var renderContext = {
      //       canvasContext: context,
      //       viewport: viewport
      //     };
      //     var renderTask = page.render(renderContext);
      //     renderTask.promise.then(function () {
      //       console.log('Page rendered');
      //     });
      //   });
      // })

      //Endd
    }
  })
})