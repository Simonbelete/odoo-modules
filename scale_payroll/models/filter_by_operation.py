from odoo import models, fields, api


class FilterByOperation(models.Model):
    _inherit = 'mrp.routing.workcenter'
    product_id = fields.Char(string="Product ID")