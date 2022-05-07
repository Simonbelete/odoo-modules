# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class stadia_HR(models.Model):
#     _name = 'stadia_HR.stadia_HR'
#     _description = 'stadia_HR.stadia_HR'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
