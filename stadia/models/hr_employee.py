from odoo import fields, api, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def action_create_user(self):
        """ Check the employee job position and create user base on that"""
        return

    def _compute_promotion_count(self):
        print('abcd')