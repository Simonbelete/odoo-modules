odoo.define('esign.pdf_edit', function (require) {
'use strict';

var core = require('web.core');
var QWeb = core.qweb;
var AbstractAction = require('web.AbstractAction');
// const { jsPDF } = require("jspdf");

var pdf_edit = AbstractAction.extend({
	start: function () {
		var self = this;

    

		// self.$('.o_content').append(QWeb.render('esing_body', {widget: self}))
		// console.log('Started')
		
    // // 698
    // // 330

    // $( function() {
    //   $( "#drag_button" ).draggable({
    //     drag: function() {
    //       var offset = $('#drag_button').offset();
    //       var xPos = offset.left;
    //       var yPos = offset.top;
    //       console.log(xPos);
    //       console.log(yPos);
    //       console.log('----------------------')
    //     }
    //   })
    //   $('#container').droppable()
    // } );

		// var url = 'esign/static/src/js/helloworld.pdf';

    // var loadingTask = pdfjsLib.getDocument(url);
    // loadingTask.promise.then(function(pdf) {
    //   var pageNumber = 1;
    //   pdf.getPage(pageNumber).then(function(page) {
    //     console.log('Page loaded');

    //     var container = $('#container')[0];
        
    //     var scale = 1.5;
    //     var viewport = page.getViewport({scale: scale});
    //     var div = document.createElement("div");

    //      // Set id attribute with page-#{pdf_page_number} format
    //      div.setAttribute("id", "page-" + (page.pageIndex + 1));

    //      // This will keep positions of child elements as per our needs
    //      div.setAttribute("style", "position: relative");
 
    //      // Append div within div#container
    //      container.appendChild(div);

    //     // Create a new Canvas element
    //     var canvas = document.createElement("canvas");
    //     var context = canvas.getContext('2d');
    //     canvas.height = viewport.height;
    //     canvas.width = viewport.width;

    //     // Append Canvas within div#page-#{pdf_page_number}
    //     div.appendChild(canvas);

    //     // Render PDF page into canvas context
    //     var renderContext = {
    //       canvasContext: context,
    //       viewport: viewport
    //     };
    //     var renderTask = page.render(renderContext);
    //     renderTask.promise.then(function () {
    //       // Get text-fragments
    //       return page.getTextContent();
    //     }).then(function(textContent) {
    //        // Create div which will hold text-fragments
    //       var textLayerDiv = document.createElement("div");

    //       // Set it's class to textLayer which have required CSS styles
    //       textLayerDiv.setAttribute("class", "textLayer");

    //       // Append newly created div in `div#page-#{pdf_page_number}`
    //       div.appendChild(textLayerDiv);

    //       // Create new instance of TextLayerBuilder class
    //       var textLayer = new pdfjsViewer.TextLayerBuilder({
    //         textLayerDiv: textLayerDiv, 
    //         pageIndex: page.pageIndex,
    //         viewport: viewport,
    //         eventBus: new pdfjsViewer.EventBus()
    //       });

    //       // Set text-fragments
    //       textLayer.setTextContent(textContent);

    //       // Render text-fragments
    //       textLayer.render();
    //     })

    //     const doc = new jspdf.jsPDF();

    //     console.log($('#container')[0])

    //     // doc.html('<div>Hellow world</div>', {
    //     //   x: 10,
    //     //   y: 10
    //     // })

    //     window.html2canvas = jspdf.html2canvas;
    //     doc.html(document.body, {
    //       callback: function (doc) {
    //         doc.save();
    //       },
    //       x: 10,
    //       y: 10
    //    })

    //     doc.text("Hello world!", 20, 30);
    //     // doc.save()

    //     div.appendChild($('#drag_button')[0])
    //   });
    // })



    // const doc = new jspdf.jsPDF();

    // doc.text("Hello world!", 10, 10);
    // doc.text("ListBox:", 10, 115);
    // var listbox = new jspdf.AcroForm.ListBox();
    // listbox.edit = false;
    // listbox.fieldName = "ChoiceField2";
    // listbox.topIndex = 2;
    // listbox.Rect = [50, 110, 30, 10];
    // listbox.setOptions(["c", "a", "d", "f", "b", "s"]);
    // listbox.value = "s";
    // doc.addField(listbox);

    // url = doc.output('bloburi')

    // url = 'esign/static/src/js/helloworld.pdf'

    // var loadingTask = pdfjsLib.getDocument(url);
    // loadingTask.promise.then(function(pdf) {

    //   var page_num = 1;
    //   pdf.getPage(page_num).then(function(page) {
        
    //     var scale = 1.5;
    //     var viewport = page.getViewport(scale);
    //     var canvas = $('#pdf-js-viewer')[0];
    //     var context = canvas.getContext('2d');
    //     canvas.height = viewport.height;
    //     canvas.width = viewport.width;

    //     var canvasOffset = $(canvas).offset();
    //     var $textLayerDiv = $('#text-layer').css({
    //         height : viewport.height+'px',
    //         width : viewport.width+'px',
    //         top : canvasOffset.top,
    //         left : canvasOffset.left
    //     });

    //     page.render({
    //         canvasContext : context,
    //         viewport : viewport
    //     });

    //     page.getTextContent().then(function(textContent){
    //        console.log( textContent );
    //         var textLayer = new pdfjsViewer.TextLayerBuilder({
    //             textLayerDiv : $textLayerDiv.get(0),
    //             pageIndex : page_num - 1,
    //             viewport : viewport,
    //             eventBus: new pdfjsViewer.EventBus()
    //         });

    //         textLayer.setTextContent(textContent);
    //         textLayer.render();
    //     });
        

    //   })
    // });

		// End

	}
});

core.action_registry.add('esign_pdf_edit_reg', pdf_edit);

return pdf_edit;

});