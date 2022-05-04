# -*- coding: utf-8 -*-
# from odoo import http


# class Odoo-asset(http.Controller):
#     @http.route('/Stadia-Asset-Management/Stadia-Asset-Management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/Stadia-Asset-Management/Stadia-Asset-Management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('Stadia-Asset-Management.listing', {
#             'root': '/Stadia-Asset-Management/Stadia-Asset-Management',
#             'objects': http.request.env['Stadia-Asset-Management.Stadia-Asset-Management'].search([]),
#         })

#     @http.route('/Stadia-Asset-Management/Stadia-Asset-Management/objects/<model("Stadia-Asset-Management.Stadia-Asset-Management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('Stadia-Asset-Management.object', {
#             'object': obj
#         })
