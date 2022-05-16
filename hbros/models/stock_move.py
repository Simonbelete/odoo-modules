from odoo import fields, api, models

class StockMove(models.Model):
    _inherit = 'stock.move'

    # From product template
    standard_price = fields.Float(related='product_tmpl_id.standard_price')
    # Raw * CONSUMTION
    consumption_cost = fields.Float(compute="_compute_consumption_cost", store=True)
    total_consumption_cost = fields.Float(compute="_compute_total_consumption_cost", store=True)

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
    production_qty = fields.Float(related="raw_material_production_id.product_qty")
    # production_qty = fields.Float(related="production_id.product_qty")

    @api.depends('standard_price')
    def _compute_consumption_cost(self):
        for record in self:
            if(record.state != 'done'):
                record.consumption_cost = record.standard_price * record.product_uom_qty

    @api.depends('standard_price', 'consumption_cost')
    def _compute_total_consumption_cost(self):
        for record in self:
            print("******************************************")
            print(record.consumption_cost)
            print(record.production_qty)
            print(record.state)
            print("************************************")
            if(record.state != 'done'):
                record.total_consumption_cost = record.production_qty * record.consumption_cost