odoo.define('esign.sign_builder', function (require) {
    'use strict';

    var core = require('web.core');
    var QWeb = core.qweb;
    var AbstractAction = require('web.AbstractAction');

    var sign_builder = AbstractAction.extend({
        start: function () {
            var url = 'esign/static/src/js/helloworld.pdf'
            this.renderBody();
            this.setupGlobalVars();
            this.displayPdf(url);
        },
        setupGlobalVars: function () {
            this.$container = this.$('#container')[0];
        },
        renderBody: function () {
            this.$('.o_content').append(QWeb.render('sign_builder_body', {Widget: this}))
        },
        displayPdf: function (url) {
            pdfjsLib.getDocument(url).promise.then(this.renderPages.bind(this))
        },
        renderPages: function (pdf) {
            var self = this;
            // Loop through pages and render it
            for (var i = 1; i <= pdf.numPages; i++) {
                pdf.getPage(i).then(this.renderPage.bind(this))
            }
        }, 
        renderPage: function (page) {
            var self = this;
            var scale = 1.5;
            var viewport = page.getViewport({scale: scale});
            var div = document.createElement("div");

            // Set id attribute with page-#{pdf_page_number} format
            div.setAttribute("id", "page-" + (page._pageIndex + 1));
            // Append div within div#container
            this.$container.appendChild(div);

            // Create a new Canvas element
            var canvas = document.createElement("canvas");
            var context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;

            // Append Canvas within div#page-#{pdf_page_number}
            div.appendChild(canvas);

            // Render PDF page into canvas context
            var renderContext = {
              canvasContext: context,
              viewport: viewport
            };

            page.render(renderContext).promise.then(function () {
                return page.getTextContent();
            }).then(function (textContent) { self.renderTextLayer({ textContext: textContent, div: div, viewport: viewport, page: page }) })
        },
        renderTextLayer: function ({textContext, div, viewport, page}) {
            // Create div which will hold text-fragments
            var textLayerDiv = document.createElement("div");

            // Set it's class to textLayer which have required CSS styles
            textLayerDiv.setAttribute("class", "textLayer");

            // Append newly created div in `div#page-#{pdf_page_number}`
            div.appendChild(textLayerDiv);

            // Create new instance of TextLayerBuilder class
            var textLayer = new pdfjsViewer.TextLayerBuilder({
                textLayerDiv: textLayerDiv, 
                pageIndex: page._pageIndex,
                viewport: viewport,
                eventBus: new pdfjsViewer.EventBus()
            });

            console.log(textContext)

            // Set text-fragments
            textLayer.setTextContent(textContext);

            // Render text-fragments
            textLayer.render();
        }
    });

    core.action_registry.add('sign_builder_registry', sign_builder);
    return sign_builder;
});