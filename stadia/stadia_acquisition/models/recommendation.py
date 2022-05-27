from odoo import fields, api, models

class Recommendation(models.Model):
    """ Recommendation either internal or external with cv including """
    _name = "stadia.acquisition.recommendation"

    ## Applicants name
    name = fields.Char(compute="_compute_name_from_employee", store=True)
    employee_id = fields.Many2one('hr.employee')
    acquisition_id = fields.Many2one('stadia.acquisition.acquisition')
    note = fields.Text()
    cv_files = fields.Binary()
    email = fields.Char()

    @api.depends('employee_id')
    def _compute_name_from_employee(self):
        for record in self:
            record.name = record.employee_id