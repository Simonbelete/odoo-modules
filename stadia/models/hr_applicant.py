from odoo import fields, api, models

class HrRecruitmentStage(models.Model):
    _inherit = 'hr.recruitment.stage'

    survey_id = fields.Many2one('survey.survey')

class HrApplicant(models.Model):
    """ Inherited modes to add is the applicant type is recommendation or not"""
    _inherit = 'hr.applicant'

    def _default_ref_no(self):
        return self.env['ir.sequence'].next_by_code('ref.no.sequence')

    ref_no = fields.Char(string="Ref No", copy=False, default=_default_ref_no, required=True)
    recommended_by = fields.Many2one('hr.employee')
    acquisition_id = fields.Many2one('stadia.acquisition', domain="[('state', '=', 'approved')]", required=True)
    survey_answer_ids = fields.One2many('applicant.answer', 'hr_applicant_id')

    @api.onchange('partner_name')
    def onchange_applicants_name(self):
        if not self.partner_name:
            return
        self.name = '%s Application letter for %s position' %(self.partner_name, self.job_id.name)

    @api.model
    def create(self, values):
        """ Populate survery for all stages """
        applicant = super(HrApplicant, self).create(values)
        applicant.sudo()._populate_survey()
        return applicant

    def _populate_survey(self):
        self.ensure_one()
        stages = self.env['stadia.promotion.stage'].search([])
        commands = []
        for s in stages:
            val = {
                'hr_applicant_id': self.id,
                'stage_id': s.id
            }
            commands.append((0, False, val))
        self.write({'survey_answer_ids': commands})


class HrApplicantAnswer(models.Model):
    _name = 'applicant.answer'

    hr_applicant_id = fields.Many2one('hr.applicant')
    stage_id = fields.Many2one('hr.recruitment.stage')
    survey_id = fields.Many2one(related="stage_id.survey_id")
    response_id = fields.Many2one('survey.user_input', "Response", ondelete="set null")

    def action_start_survey(self):
        self.ensure_one()
        if not self.response_id:
            response = self.survey_id._create_answer(user=self.env.user)
            self.response_id = response.id
        else:
            response = self.response_id

        return self.survey_id.action_start_survey(answer=response)

    def action_print_survey(self):
        self.ensure_one()
        return self.survey_id.action_print_survey(answer=self.response_id)