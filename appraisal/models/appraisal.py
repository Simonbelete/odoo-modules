from odoo import fields, api, models

class Appraisal(models.Model):
    """ Appraisal for each employee yearly or 6 moths. """
    _name = 'appraisal.appraisal'
    _description = 'Appraisal'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string = 'Employee')