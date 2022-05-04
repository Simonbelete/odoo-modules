# -*- coding: utf-8 -*-
from odoo import http


class EmployeeMs(http.Controller):
    @http.route('/stadia_HR/stadia_HR/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/stadia_HR/stadia_HR/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('stadia_HR.listing', {
            'root': '/stadia_HR/stadia_HR',
            'objects': http.request.env['stadia_HR.stadia_HR'].search([]),
        })

    @http.route('/stadia_HR/stadia_HR/objects/<model("stadia_HR.stadia_HR"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('stadia_HR.object', {
            'object': obj
        })
