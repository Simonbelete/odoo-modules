from odoo import models, fields, api


class FilterByOperation(models.Model):
    _inherit = 'mrp.bom.line'
    consumition_qty = fields.Float(string="Consumtion")
