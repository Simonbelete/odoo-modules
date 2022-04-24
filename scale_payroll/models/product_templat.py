from odoo import models, fields, api


class FilterByOperation(models.Model):
    _inherit = 'product.template'
    specification = fields.Char(string="Specification")
    group = fields.Char(string="Product Group")
    type2 = fields.Char(string="Type")
