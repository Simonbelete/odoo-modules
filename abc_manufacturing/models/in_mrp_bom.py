from odoo import models, fields, api

class InMrpBom(models.Model):
    _inherit = 'mrp.bom.line'

    cost = fields.Float(related = 'product_id.standard_price')