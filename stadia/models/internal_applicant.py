from odoo import api, fields, models

class InternalApplicant(models.Model):
    """ In company applicants list"""
    _name = "stadia.internal.applicant"
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', required=True)
    # Select opend job positions
    job_id = fields.Many2one('hr.job', domain="[('state', '=', 'recruit')]", required=True)