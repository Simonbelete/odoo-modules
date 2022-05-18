# -*- coding: utf-8 -*-
# from odoo import http


# class Asset-management(http.Controller):
#     @http.route('/asset-management/asset-management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asset-management/asset-management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asset-management.listing', {
#             'root': '/asset-management/asset-management',
#             'objects': http.request.env['asset-management.asset-management'].search([]),
#         })

#     @http.route('/asset-management/asset-management/objects/<model("asset-management.asset-management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asset-management.object', {
#             'object': obj
#         })
