from odoo import api, fields, models

class InternalApplicant(models.Model):
    """ In company applicants list"""
    _name = "stadia.internal.applicant"

    employee_id = fields.Many2one('hr.employee')
    job_id = fields.Many2one('hr.job')