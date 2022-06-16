from odoo import fields, api, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    family_ids = fields.One2many('hr.employee.family', 'employee_id')

    def action_create_user(self):
        """ Check the employee job position and create user base on that"""
        return

    def _compute_promotion_count(self):
        print('abcd')