from odoo import fields, api, models

class StockMove(models.Model):
    _inherit = 'stock.move'

    # From product template
    standard_price = fields.Float(related='product_tmpl_id.standard_price')
    # Raw * CONSUMTION
    consumption_cost = fields.Float(compute="_compute_consumption_cost")

    # Reference Fields from product.template
    product_type = fields.Many2one(
        'hbros.product.type', 'Product Type',
        related="product_tmpl_id.product_type", readonly=True
    )
    product_specification = fields.Many2one(
        'hbros.product.specification', 'Product Specification',
        related="product_tmpl_id.product_specification", readonly=True
    )
    measurement_uom_id = fields.Many2one(
        'uom.uom', 'Measurement',
        related="product_tmpl_id.measurement_uom_id", readonly=True
    )

    @api.depends('standard_price')
    def _compute_consumption_cost(self):
        for record in self:
            print('-----------------------------')
            print(record.product_uom_qty)
            print('-----------------------------')
            record.consumption_cost = record.standard_price * record.product_uom_qty
