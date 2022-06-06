from odoo import fields, api, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    title = fields.Selection([
        ('ato', 'Ato'),
        ('wt', 'W/t'),
        ('wro', 'W/ro')
    ], required=True)
    promotion_count = fields.Integer(default=0)

    def action_create_user(self):
        """ Check the employee job position and create user base on that"""
        return

    def _compute_promotion_count(self):
        print('abcd')