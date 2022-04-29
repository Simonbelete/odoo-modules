from odoo import models, fields

class Appraisal(models.Model):
    _name = 'appraisal.appraisal'

    employee_id = fields.Many2one('hr.employee', string = 'Employee')
    survey_id = fields.Many2one('appraisal.survey')
    appraisal_score_ids = fields.One2many('appraisal.appraisal.score', 'appraisal_id')

    def button_confirm_appraisal(self):
        return True