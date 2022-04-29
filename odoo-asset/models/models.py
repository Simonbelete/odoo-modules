# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class odoo-asset(models.Model):
#     _name = 'odoo-asset.odoo-asset'
#     _description = 'odoo-asset.odoo-asset'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
