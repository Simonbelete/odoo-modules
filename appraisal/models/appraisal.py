from odoo import models, fields, api

class Appraisal(models.Model):
    _name = 'appraisal.appraisal'

    employee_id = fields.Many2one('hr.employee', string = 'Employee')
    survey_id = fields.Many2one('appraisal.survey')
    appraisal_score_ids = fields.One2many('appraisal.appraisal.score', 'appraisal_id')

    def button_confirm_appraisal(self):
        questions = self.env['appraisal.survey.question'].search([('survey_ids', 'in', self.survey_id.id )])
        for q in questions:
            record = self.env['appraisal.appraisal.score'].create({
                'appraisal_id': self.id,
                'survey_question_id': q.id,
                'score': 0
            })
        #     self.write({'appraisal_score_ids': [self.appraisal_score_ids, record.id]})