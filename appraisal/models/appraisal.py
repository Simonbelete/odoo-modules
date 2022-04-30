from odoo import models, fields, api

class Appraisal(models.Model):
    _name = 'appraisal.appraisal'

    name = fields.Text(compute="_generate_name_for_appraisal")
    employee_id = fields.Many2one('hr.employee', string = 'Employee')
    survey_id = fields.Many2one('appraisal.survey')
    appraisal_score_ids = fields.One2many('appraisal.appraisal.score', 'appraisal_id')
    state = fields.Selection(string="Status", required=True, readonly=True, copy=False, tracking=True, selection=[
        ('draft', 'To Confirm'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done')
    ], default="draft",
    help="The current state of the appraisal:"
         "- To Confirm: Newly created appraisal")

    def button_confirm_appraisal(self):
        questions = self.env['appraisal.survey.question'].search([('survey_ids', 'in', self.survey_id.id )])
        for q in questions:
            record = self.env['appraisal.appraisal.score'].create({
                'appraisal_id': self.id,
                'survey_question_id': q.id,
                'score': 0
            })

    # TODO: Add date
    @api.depends('employee_id')
    def _generate_name_for_appraisal(self):
        for record in self:
            record.name = record.employee_id.name
