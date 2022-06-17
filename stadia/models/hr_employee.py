from odoo import fields, api, models



class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    joining_date = fields.Date(string='Joining Date', help="Employee joining date computed from the contract start date",compute='_compute_joining', store=True)
    work_place_id = fields.Many2one(related='contract_id.work_place_id')

    @api.depends('contract_id')
    def _compute_joining(self):
        if self.contract_id:
            date = min(self.contract_id.mapped('date_start'))
            self.joining_date = date
        else:
            self.joining_date = False

    def action_create_user(self):
        """ Check the employee job position and create user base on that"""
        return

    def _compute_promotion_count(self):
        print('abcd')