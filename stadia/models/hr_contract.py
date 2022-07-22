from odoo import fields, api, models
from datetime import datetime
from dateutil.relativedelta import relativedelta
from num2words import num2words

class HrContract(models.Model):
    _inherit = 'hr.contract'

    # def _default_work_place_id(self):
    #     return self.env['stadia.workplace'].search([('name', '=', 'Head Office')], limit=1)

    def _default_ref_no(self):
        return self.env['ir.sequence'].next_by_code('ref.no.sequence')

    ref_no = fields.Char(string="Ref No", copy=False, default=_default_ref_no)
    # Per day perdime
    perdime = fields.Monetary(default=0)
    perdime_in_word = fields.Char(compute="_compute_perdime_in_word")
    cost_sharing = fields.Monetary(default=0)
    phone_allowance = fields.Monetary(default=0, string="Phone Allowance")
    cost_sharing = fields.Monetary(default = 0)
    work_place_id = fields.Many2one('stadia.workplace', required=True) #, default=_default_work_place_id)
    transport_allowance = fields.Monetary(default=0)
    transport_allowance_in_word = fields.Char(compute="_compute_transport_allowance_in_word")
    desert_allowance = fields.Monetary(default=0)
    desert_allowance_in_word = fields.Char(compute="_compute_desert_allowance_in_word")
    wage_in_word = fields.Char(compute="_compute_wage_in_word")

    # For printing
    issued_date = fields.Date(compute="_compute_issued_date")
    expiry_date = fields.Date(compute="_compute_expiry_date")

    def _compute_transport_allowance_in_word(self):
        self.ensure_one()
        self.transport_allowance_in_word = num2words(self.transport_allowance)

    def _compute_perdime_in_word(self):
        self.ensure_one()
        self.perdime_in_word = num2words(self.perdime)

    def _compute_desert_allowance_in_word(self):
        self.ensure_one()
        self.desert_allowance_in_word = num2words(self.desert_allowance)

    def _compute_wage_in_word(self):
        self.ensure_one()
        self.wage_in_word = num2words(self.wage)

    def _compute_issued_date(self):
        self.issued_date = datetime.now()

    def _compute_expiry_date(self):
        self.expiry_date = datetime.now() + relativedelta(years=1)

    # Override default
    @api.depends('employee_id')
    def _compute_employee_contract(self):
        for contract in self.filtered('employee_id'):
            # contract.job_id = contract.employee_id.job_id
            contract.department_id = contract.employee_id.department_id
            contract.resource_calendar_id = contract.employee_id.resource_calendar_id
            contract.company_id = contract.employee_id.company_id
