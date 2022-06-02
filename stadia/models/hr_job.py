from odoo import fields, api, models

class Job(models.Model):
    _inherit = 'hr.job'

    promotion_count = fields.Integer(compute="_compute_promotion_count")

    def _compute_promotion_count(self):
        stage = self.env['stadia.promotion.stage'].search([('name', '!=', 'Waiting')])
        
        promotions = 0
        # if(stage.ids):
        #     self.env['stadia.promotion'].search_count([
        #         ('job_id', '=', self.id),
        #         ('state_id', 'in', stage.ids)
        #     ])  
        for record in self:
            record.promotion_count = promotions