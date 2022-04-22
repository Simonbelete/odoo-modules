from odoo import models, fields, api

class InMrpBom(models.Model):
    _inherit = 'mrp.bom.line'

    # cost = fields.Float(related = 'product_id.standard_price')
    cost = fields.Float(required = True, digits='Product Price')
    total_cost = fields.Float(compute="_compute_total_cost", digits='Product Price')

    # inherited comes second field
    @api.depends('cost', 'product_qty')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.product_qty * record.cost

    # Compute cost based on quanity
    # @api.depends('product_qty')
    # def _compute_cost(self):
    #     for record in self:
    #         # record.cost =  record.product_qty / record.product_id.standard_price
    #         record.cost =  record.product_qty