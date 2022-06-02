from odoo import fields, api, models

class HrApplicant(models.Model):
    """ Inherited modes to add is the applicant type is recommendation or not"""
    _inherit = 'hr.applicant'

    recommended_by = fields.Many2one('hr.employee')
    acquisition_id = fields.Many2one('stadia.acquisition', domain="[('state', '=', 'approved')]", required=True)