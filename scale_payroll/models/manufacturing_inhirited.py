from odoo import models, fields, api


class ManufacturingInhirited(models.Model):
    _inherit = 'mrp.production'
    product_type = fields.Selection(
        [('for next use', 'For next use'),
         ('final product', 'Final Product')],
        default='final product')
    price = fields.Integer(string="Tip for single Item")
    calculated_price = fields.Integer(compute="calculatedPrice", string="Total Tip Price for Employee", store=True)
    emp_id = fields.Many2one('hr.employee', string="Employee", required="True")
    mrp_production_contract = fields.Many2one('hr.contract', string=" MRP-CONTRACT")

    @api.depends('price', 'product_qty')
    def calculatedPrice(self):
        for prodct_price in self:
            prodct_price.calculated_price = prodct_price.product_qty * prodct_price.price
