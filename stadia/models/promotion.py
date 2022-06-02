from odoo import fields, api, models

class Promotion(models.Model):
    """ Internal Employee promotions """
    _name = 'stadia.promotion'

    employee_id = fields.Many2one('hr.employee')
    department_id =  fields.Many2one(related="employee_id.department_id")
    job_id = fields.Many2one(related="employee_id.job_id")
    stage_id = fields.Many2one('stadia.promotion.stage', group_expand="_read_group_state_ids")

    @api.model
    def _read_group_state_ids(self, stages, domain, order):
        stage_ids = stages._search([],order=order)
        return stages.browse(stage_ids)