from odoo import fields, api, models
from datetime import datetime
from num2words import num2words

class Promotion(models.Model):
    """ Internal Employee promotions """
    _name = 'stadia.promotion'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _default_stage_id(self):
        return self.env['stadia.promotion.stage'].search([('sequence', '=', 1)], limit=1)

    def _default_ref_no(self):
        return self._generate_ref_no()

    def _generate_ref_no(self):
        return self.env['ir.sequence'].next_by_code('ref.no.sequence')

    ref_no = fields.Char(string="Ref No", copy=False, default=_default_ref_no, required=True)
    # Employee to be promoted
    employee_id = fields.Many2one('hr.employee')
    start_date = fields.Date(required=True, default=datetime.now())
    department_id =  fields.Many2one(related="employee_id.department_id")
    # Previous job id
    job_id = fields.Many2one(related="employee_id.job_id")
    # Active previous work location
    active_work_place_id = fields.Many2one(related="employee_id.contract_id.work_place_id")
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
    salary = fields.Monetary(default=0)
    salary_in_word = fields.Char(compute="_compute_salary_in_word")
    perdime = fields.Monetary(default=0)
    perdime_in_word = fields.Char(compute="_compute_perdime_in_word")
    allowance = fields.Monetary(default=0)
    allowance_in_word = fields.Char(compute="_compute_allowance_in_word")
    transport_allowance = fields.Monetary(default=0)
    transport_allowance_in_word = fields.Char(compute="_compute_transport_allowance_in_word")
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  readonly=True,
        default=lambda self: self.env.user.company_id.currency_id.id)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 readonly=True,
                                 default=lambda self: self.env.company)

    def _compute_salary_in_word(self):
        self.ensure_one()
        self.salary_in_word = num2words(self.salary)

    def _compute_perdime_in_word(self):
        self.ensure_one()
        self.perdime_in_word = num2words(self.perdime)

    def _compute_allowance_in_word(self):
        self.ensure_one()
        self.allowance_in_word = num2words(self.allowance)

    def _compute_transport_allowance_in_word(self):
        self.ensure_one()
        self.transport_allowance_in_word = num2words(self.transport_allowance)

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
        self.write({'survey_answer_ids': commands})

    @api.model
    def _read_group_state_ids(self, stages, domain, order):
        stage_ids = stages._search([],order=order)
        return stages.browse(stage_ids)

    def action_open_hr_contract_form(self):
        return {
            'res_model': 'hr.contract',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref('stadia.stadia_hr_employee_contract_form').id,
            'target': 'self',
            'context': {
                'default_wage': self.salary,
                'default_employee_id': self.employee_id.id,
                'default_job_id': self.new_designation_job_id.id,
                'default_date_start': self.start_date,
                'default_perdime': self.perdime,
                'default_other_allowance': self.allowance,
                'default_transport_allowance': self.transport_allowance
            }
        }


class PromotionStageSurvery(models.Model):
    _name = 'promotion.answer'

    promotion_id = fields.Many2one('stadia.promotion')
    stage_id = fields.Many2one('stadia.promotion.stage')
    survey_id = fields.Many2one(related='stage_id.survey_id')
    response_id = fields.Many2one('survey.user_input', "Response", ondelete="set null")
    
    def action_start_survey(self):
        self.ensure_one()
        if not self.response_id:
            response = self.survey_id._create_answer(user=self.env.user)
            self.response_id = response.id
        else:
            response = self.response_id
        ## TODO: Display user error when stage doesn't have survery selected
        return self.survey_id.action_start_survey(answer=response)

        # for record in self:
        #     if not record.response_id:
        #         response = self.survey_id._create_answer(user=record.env.user)
        #         record.response_id = response.id
        #     else:
        #         response = self.response_id

        #     return record.survey_id.action_start_survey(answer=response)

    def action_print_survey(self):
        self.ensure_one()
        return self.survey_id.action_print_survey(answer=self.response_id)