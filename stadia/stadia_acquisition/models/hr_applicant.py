from odoo import fields, api, models

class HrApplicant(models.Model):
    """ Inherited modes to add is the applicant type is recommendation or not"""
    _inherit = 'hr.applicant'

    acquisition_id = fields.Many2one('stadia.acquisition.acquisition', required=True)
    ## Employee id if the applicant is internal
    employee_id = fields.Many2one('hr.employee')
    applicant_type = fields.Selection([
        ('internal', 'Internal'),
        ('external', 'External')
    ], default='external',
    help="internal - an employed in the company for either promotion or transfer"
        "external - from outside applicant")