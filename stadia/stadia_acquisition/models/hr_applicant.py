from odoo import fields, api, models

class HrApplicant(models.Model):
    """ Inherited modes to add is the applicant type is recommendation or not"""
    _inherit = 'hr.applicant'

    recommended_by = fields.Many2one('hr.employee')
    acquisition_id = fields.Many2one('stadia.acquisition.acquisition')
    ## Employee id if the applicant is internal
    employee_id = fields.Many2one('hr.employee')
    application_type = fields.Selection([
        ('internal', 'Internal'),
        ('external', 'External')
    ], default='external')

    @api.onchange('partner_name')
    def onchange_applicants_name(self):
        if not self.partner_name:
            return
        self.name = '%s Application letter for %s position' %(self.partner_name, self.job_id.name)
        self.application_type = 'external'
    
    def _compute_is_internal(self):
        if(not self.employee_id):
            self.application_type = 'external'
        else:
            self.application_type = 'internal'

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        """ Auto Populate the hr applicants fields"""
        if(not self.employee_id):
            return
        
        self.application_type = 'internal'
        self.name = '%s Application letter for %s position' %(self.employee_id.name, self.job_id.name)
        self.partner_name = self.employee_id.name
        self.email_from = self.employee_id.work_email