from odoo import fields, api, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    promotion_count = fields.Integer(compute="_compute_promotion_count")

    def _compute_promotion_count(self):
        """ Count approved promotions """
        for record in self:
            record.promotion_count = self.env['stadia.promotion.promotion'].search_count([('id', '=', record.id), ('state', '=', 'approved')])