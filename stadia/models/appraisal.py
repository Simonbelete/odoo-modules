from odoo import fields, api, models

class Appraisal(models.Model):
    _name = 'stadia.appraisal'

    employee_id = fields.Many2one('hr.employee', required=True)
    