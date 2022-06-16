from odoo import fields, api, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    family_ids = fields.One2many('hr.employee.family', 'employee_id')
    emergency_contact_name = fields.Char()
    emergency_contact_city_id = fields.Many2one('subcity')
    emergency_contact_woreda = fields.Char()
    emergency_contact_house_no = fields.Char()
    emergency_contact_relation_id = fields.Many2one('hr.employee.relation')

    def action_create_user(self):
        """ Check the employee job position and create user base on that"""
        return

    def _compute_promotion_count(self):
        print('abcd')