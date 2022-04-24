# -*- coding: utf-8 -*-
# from odoo import http


# class ScalePayroll(http.Controller):
#     @http.route('/scale_payroll/scale_payroll/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/scale_payroll/scale_payroll/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('scale_payroll.listing', {
#             'root': '/scale_payroll/scale_payroll',
#             'objects': http.request.env['scale_payroll.scale_payroll'].search([]),
#         })

#     @http.route('/scale_payroll/scale_payroll/objects/<model("scale_payroll.scale_payroll"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('scale_payroll.object', {
#             'object': obj
#         })
