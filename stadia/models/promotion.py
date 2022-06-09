from odoo import fields, api, models

class Promotion(models.Model):
    """ Internal Employee promotions """
    _name = 'stadia.promotion'
    _res_name = 'employee_id'

    def _default_stage_id(self):
        a = self.env['stadia.promotion.stage'].search([('sequence', '=', 1)], limit=1)
        print('11111111111111111111111111111')
        return a

    # Employee to be promoted
    employee_id = fields.Many2one('hr.employee')
    department_id =  fields.Many2one(related="employee_id.department_id")
    # Previous job id
    job_id = fields.Many2one(related="employee_id.job_id")
    stage_id = fields.Many2one('stadia.promotion.stage', group_expand="_read_group_state_ids", default=_default_stage_id)
    acquisition_id = fields.Many2one('stadia.acquisition', domain="[('state', '=', 'approved')]")
    recommended_by = fields.Many2one('hr.employee')
    new_designation_job_id = fields.Many2one('hr.job', required=True)
    active = fields.Boolean(default=True)
    promotion_type = fields.Selection([
        ('promotion', 'Promotion'),
        ('transfer', 'Transfer')
    ], default='promotion')

    @api.model
    def _read_group_state_ids(self, stages, domain, order):
        stage_ids = stages._search([],order=order)
        return stages.browse(stage_ids)