from odoo import models, fields, api

class InStockMove(models.Model):
    _inherit = 'stock.move'

    cost_history = fields.Float(compute="_compute_get_cost_from_bom_line", store = False, digits='Product Price')
    total_cost = fields.Float(compute="_compute_total_cost", digits='Product Price')

    # Triger when production is done or created
    # copy from bom_line for history, so that changing bom cost 
    # doesn't affect previous manufactured orders
    @api.depends('is_done', 'raw_material_production_id', 'production_id')
    def _compute_get_cost_from_bom_line(self):
        for record in self:
            record.cost_history = record.bom_line_id.cost
    
    @api.depends('cost_history', 'bom_line_id.product_qty')
    def _compute_total_cost(self):
        for record in self:
            print('-----------------------------')
            print(record.product_uom_qty)
            print('-----------------------------')
            record.total_cost = record.product_uom_qty * record.cost_history