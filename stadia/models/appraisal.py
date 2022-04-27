from odoo import models, fields

class Appraisal(models.Model):
    _name = 'stadia.appraisal.appraisal'

    employee_id = fields.Many2one('res.users', string = 'Employee')
    rated_by_id = fields.Many2one('res.users', string = 'Rated by')
    approved_by_id = fields.Many2one('res.users', string = 'Approved by')
    job_location = fields.Char()
    date = fields.Date()
    last_evaluation = fields.Date()
    appraisal_score_ids = fields.One2many('stadia.appraisal.score', '')
    strengths = fields.Text() # Comment on principal strengths:
    suggestion = fields.Text() # Comment on principal weaknesses and suggestions for improvement
    is_discussed_with_employee = fields.Boolean(required = True)
    recommendation = fields.Text() # Your recommendation for present and future job classification

    # Signatures
    employee_signature = fields.Char()
    employee_signature_date = fields.Date()