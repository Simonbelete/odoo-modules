from odoo import fields, api, models
from odoo.tools.safe_eval import datetime


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    work_place_id = fields.Many2one(related='contract_id.work_place_id', store=True)
    promotion_count = fields.Integer(default=0, compute="_compute_promotion_count")
    asset_count = fields.Integer(default=0, compute="_compute_asset_count")

    def _compute_asset_count(self):
        self.ensure_one()
        asset_count = self.env['stadia.asset'].search_count([('current_movement_employee_id', '=', self.id)])
        self.asset_count = asset_count

    def _compute_promotion_count(self):
        self.ensure_one()
        last_stage_id = self.env['stadia.promotion.stage'].search([])
        last_stage_id = max(last_stage_id.mapped('sequence'))
        promotions_count = self.env['stadia.promotion'].search_count(
            [('employee_id', '=', self.id), ('stage_id', '=', last_stage_id)])
        self.promotion_count = promotions_count

    @api.model
    def create(self, values):
        employee = super(HrEmployee, self).create(values)
        users = self.env.ref('stadia.group_base_system_admin').users
        for user in users:
            if (user.active == True):
                employee.sudo().activity_schedule('stadia.mail_act_employee_creation', user_id=user.id,
                                                  summary='Give user acess to odoo',
                                                  note=f'Please Create credentials for {self.name} with the corresponding credentials')
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

    calculated_age = fields.Char(string="Age", compute="_calculate_age")
    print(calculated_age)

    @api.onchange('birthday')
    def _calculate_age(self):
        today = datetime.date.today()
        for data in self:
            if data.birthday:
                birthday = fields.Datetime.to_datetime(data.birthday).date()
                total_age = str(int((today - birthday).days / 365))
                data.calculated_age = total_age
            else:
                data.calculated_age = " "
