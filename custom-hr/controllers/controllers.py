# -*- coding: utf-8 -*-
# from odoo import http


# class Custom-hr(http.Controller):
#     @http.route('/custom-hr/custom-hr/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom-hr/custom-hr/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom-hr.listing', {
#             'root': '/custom-hr/custom-hr',
#             'objects': http.request.env['custom-hr.custom-hr'].search([]),
#         })

#     @http.route('/custom-hr/custom-hr/objects/<model("custom-hr.custom-hr"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom-hr.object', {
#             'object': obj
#         })
