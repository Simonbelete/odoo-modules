# -*- coding: utf-8 -*-
# from odoo import http


# class StadiaEmployeeProfile(http.Controller):
#     @http.route('/stadia_employee_profile/stadia_employee_profile/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stadia_employee_profile/stadia_employee_profile/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stadia_employee_profile.listing', {
#             'root': '/stadia_employee_profile/stadia_employee_profile',
#             'objects': http.request.env['stadia_employee_profile.stadia_employee_profile'].search([]),
#         })

#     @http.route('/stadia_employee_profile/stadia_employee_profile/objects/<model("stadia_employee_profile.stadia_employee_profile"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stadia_employee_profile.object', {
#             'object': obj
#         })
