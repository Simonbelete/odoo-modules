from odoo import models, fields, api

class HrEmployee(models.Model):
    """ From hr.hr_employee """
    _name = 'appraisal.hr.employee'
    _inherit = 'hr.employee'

    appraisal_status = fields.Selection([
        ('to start', 'To Start'),
        ('started', 'Started'),
        ('done', 'Canacled')
    ], compute="_compute_appraisal_status")
    # last_appraisal_date = fields.Date()
    
    @api.depends()
    def _compute_appraisal_status(self):
        for record in self:
            appraisals = self.env['appraisal.appraisal'].search([
                ('employee_id', '=', record.id)
            ])
            appraisal_dates = []
            last_appraisal_date = ''
            for appraisal in appraisals:
                last_appraisal_date = ''
                appraisal_dates.append(appraisal.create_date)

            