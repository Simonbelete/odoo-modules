from odoo import fields, api, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    title = fields.Selection([
        ('ato', 'Ato'),
        ('wt', 'W/t'),
        ('wro', 'W/ro')
    ], required=True)
    sex = fields.Selection([
        ('m', 'Male'),
        ('f', 'female')
    ], required=True)

    def action_create_user(self):
        """ Check the employee job position and create user base on that"""
        