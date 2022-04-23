from odoo import models, fields, api

class InStockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    cost = fields.Float(required = True, digits='Product Price')
    total_cost = fields.Float(compute="_compute_total_cost", digits='Product Price')

    # inherited comes second field
    @api.depends('cost', 'product_qty')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.product_qty * record.cost