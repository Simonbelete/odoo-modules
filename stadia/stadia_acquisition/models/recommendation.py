from odoo import fields, api, models

class Recommendation(models.Model):
    """ Recommendation either internal or external with cv including """
    _name = "stadia.acquisition.recommendation"

    employee_id = fields.Many2one('hr.employee')
    acquisition_id = fields.Many2one('stadia.acquisition.acquisition')
    note = fields.Text()
    cv_files = fields.Binary()