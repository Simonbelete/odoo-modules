# -*- coding: utf-8 -*-
# from odoo import http


# class Odoo-asset(http.Controller):
#     @http.route('/odoo-asset/odoo-asset/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo-asset/odoo-asset/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo-asset.listing', {
#             'root': '/odoo-asset/odoo-asset',
#             'objects': http.request.env['odoo-asset.odoo-asset'].search([]),
#         })

#     @http.route('/odoo-asset/odoo-asset/objects/<model("odoo-asset.odoo-asset"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo-asset.object', {
#             'object': obj
#         })
