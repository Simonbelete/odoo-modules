from odoo import fields, api, models

class Acquisition(models.Model):
    """ Acquisition Form for hiring or promoting employee """
    _name = 'stadia.acquisition.acquisition'


    job_id = fields.Many2one('hr.job')
    state = fields.Selection([
        ('open', 'Open'),
        ('done', 'Done'),
        ('cancel', 'Cancel')
    ])

    ## Below fields are for recommendation cv/employee
    recommended_employee_id = fields.Many2one('hr.employee')
    recommended_employee_salary = fields.Float()
    recommended_employee_allowance = fields.Float()
    recommended_effective_date = fields.Date()
    