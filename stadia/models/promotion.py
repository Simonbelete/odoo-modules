from odoo import fields, api, models
from datetime import datetime

class Promotion(models.Model):
    """ Internal Employee promotions """
    _name = 'stadia.promotion'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _default_stage_id(self):
        return self.env['stadia.promotion.stage'].search([('sequence', '=', 1)], limit=1)

    # Employee to be promoted
    employee_id = fields.Many2one('hr.employee')
    date = fields.Date(required=True, default=datetime.now())
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
    new_work_place = fields.Many2one('stadia.workplace')
    survey_answer_ids = fields.One2many('promotion.answer', 'promotion_id')
    
    @api.model
    def create(self, values):
        """ Auto Create/populate with survey ids """
        promotion = super(Promotion, self).create(values)
        promotion.sudo()._populate_answeres()
        return promotion

    def _populate_answeres(self):
        self.ensure_one()
        stages = self.env['stadia.promotion.stage'].search([])
        commands = []
        for s in stages:
            val = {
                'promotion_id': self.id,
                'stage_id': s.id
            }
            commands.append((0, False, val))
        print('00000000000000000000000000000')
        print(commands)
        print('00000000000000000000000000000')
        self.write({'survey_answer_ids': commands})

    @api.model
    def _read_group_state_ids(self, stages, domain, order):
        stage_ids = stages._search([],order=order)
        return stages.browse(stage_ids)


class PromotionStageSurvery(models.Model):
    _name = 'promotion.answer'

    promotion_id = fields.Many2one('stadia.promotion')
    stage_id = fields.Many2one('stadia.promotion.stage')
    survey_id = fields.Many2one(related='stage_id.survey_id')
    response_id = fields.Many2one('survey.user_input', "Response", ondelete="set null")
    
    def action_start_survey(self):
        if not self.response_id:
            response = self.survey_id._create_answer(user=self.env.user)
            self.response_id = response.id
        else:
            response = self.response_id

        return self.survey_id.action_start_survey(answer=response)

    def action_print_survey(self):
        self.ensure_one()
        return self.survey_id.action_print_survey(answer=self.response_id)