from odoo import fields, models

class StockMove(models.Model):
    _inherit = 'stock.move'

    cost = fields.Float()
