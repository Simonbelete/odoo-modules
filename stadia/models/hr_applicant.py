from odoo import fields, api, models

class HrApplicant(models.Model):
    """ Inherited modes to add is the applicant type is recommendation or not"""
    _inherit = 'hr.applicant'

    recommended_by = fields.Many2one('hr.employee')
    acquisition_id = fields.Many2one('stadia.acquisition', domain="[('state', '=', 'approved'), ('job_id', '=', job_id)]", required=True)

    @api.onchange('partner_name')
    def onchange_applicants_name(self):
        if not self.partner_name:
            return
        self.name = '%s Application letter for %s position' %(self.partner_name, self.job_id.name)