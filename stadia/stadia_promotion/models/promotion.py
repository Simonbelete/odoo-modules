from odoo import fields, api, models

class Promotion(models.Model):
    """ Employee's promotion """
    _name = 'stadia.promotion.promotion'

    employee_id = fields.Many2one('hr.employee')
    previous_designation_id = fields.Many2one('hr.job')
    new_designation_id = fields.Many2one('hr.job')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('declined', 'Declined')
    ])