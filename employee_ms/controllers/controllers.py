# -*- coding: utf-8 -*-
from odoo import http


class EmployeeMs(http.Controller):
    @http.route('/employee_ms/employee_ms/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/employee_ms/employee_ms/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('employee_ms.listing', {
            'root': '/employee_ms/employee_ms',
            'objects': http.request.env['employee_ms.employee_ms'].search([]),
        })

    @http.route('/employee_ms/employee_ms/objects/<model("employee_ms.employee_ms"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('employee_ms.object', {
            'object': obj
        })
