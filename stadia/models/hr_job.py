from odoo import fields, api, models

class Job(models.Model):
    _inherit = 'hr.job'

    promotion_count = fields.Integer(compute="_compute_promotion_count")

    def _compute_promotion_count(self):
        for record in self:
            promotion_count = self.env['stadia.promotion'].search_count([('job_id', '=', record.id)]) 
            record.promotion_count = promotion_count