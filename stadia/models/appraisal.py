from odoo import fields, api, models

class Appraisal(models.Model):
    _name = 'stadia.appraisal'
    
    survey_id = fields.Many2one('survey.survey')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')
    ])