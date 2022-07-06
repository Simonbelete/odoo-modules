from odoo import fields, api, models
from datetime import datetime
from dateutil.relativedelta import relativedelta


class HrContract(models.Model):
    _inherit = 'hr.contract'

    def _default_work_place_id(self):
        return self.env['stadia.workplace'].search([('name', '=', 'Head Office')], limit=1)

    def _default_ref_no(self):
        return self.env['ir.sequence'].next_by_code('ref.no.sequence')

    ref_no = fields.Char(string="Ref No", copy=False, default=_default_ref_no)
    # Per day perdime
    perdime = fields.Monetary(default=0)
    cost_sharing = fields.Monetary(default=0)
    phone_allowance = fields.Monetary(default=0, string="Phone Allowance")
    perdime = fields.Monetary(default = 0)
    cost_sharing = fields.Monetary(default = 0)
    work_place_id = fields.Many2one('stadia.workplace', required=True, default=_default_work_place_id)
    transport_allowance = fields.Monetary(default=0)
    desert_allowance = fields.Monetary(default=0)

    # For printing
    issued_date = fields.Date(compute="_compute_issued_date")
    expiry_date = fields.Date(compute="_compute_expiry_date")

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
