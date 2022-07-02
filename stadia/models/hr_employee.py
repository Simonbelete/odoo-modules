from odoo import fields, api, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    work_place_id = fields.Many2one(related='contract_id.work_place_id', store=True)
    promotion_count = fields.Integer(default=0, compute="_compute_promotion_count")

    def _compute_promotion_count(self):
        self.ensure_one()
        last_stage_id = self.env['stadia.promotion.stage'].search([])
        last_stage_id = max(last_stage_id.mapped('sequence'))
        promotions_count = self.env['stadia.promotion'].search_count([('employee_id', '=', self.id), ('stage_id', '=', last_stage_id)])
        self.promotion_count = promotions_count


    @api.model
    def create(self, values):
        employee = super(HrEmployee, self).create(values)
        users = self.env.ref('stadia.group_base_system_admin').users
        for user in users:
            if(user.active == True):
                employee.sudo().activity_schedule('stadia.mail_act_employee_creation', user_id=user.id, summary='Give user acess to odoo', note=f'Please Create credentials for {self.name} with the corresponding credentials')
        return employee

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