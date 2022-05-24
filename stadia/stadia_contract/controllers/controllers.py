# -*- coding: utf-8 -*-
# from odoo import http


# class StadiaContract(http.Controller):
#     @http.route('/stadia_contract/stadia_contract/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stadia_contract/stadia_contract/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stadia_contract.listing', {
#             'root': '/stadia_contract/stadia_contract',
#             'objects': http.request.env['stadia_contract.stadia_contract'].search([]),
#         })

#     @http.route('/stadia_contract/stadia_contract/objects/<model("stadia_contract.stadia_contract"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stadia_contract.object', {
#             'object': obj
#         })
