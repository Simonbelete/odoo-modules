from odoo import fields, api, models
from dateutil import relativedelta
from datetime import datetime

class HrLoan(models.Model):
    _inherit = 'hr.loan'

    reason = fields.Text()
    guarantor_id = fields.Many2one('hr.employee')
    monthly_payment = fields.Float(compute="_compute_monthly_payment")
    end_payment_date = fields.Date(compute="_compute_end_payment_date")
    no_months = fields.Integer(default=0, required=True)
    salary = fields.Monetary(related='employee_id.contract_id.wage')
    first_contract_date = fields.Date(related='employee_id.contract_id.first_contract_date')
    service_years = fields.Float(compute="_compute_service_years")

    @api.depends('employee_id')
    def _compute_service_years(self):
        self.ensure_one()
        print('333333333333333333333333333333')
        print(datetime.today())
        print(self.first_contract_date)
        if(self.first_contract_date):
            diff = relativedelta.relativedelta(datetime.today(), self.first_contract_date)
            self.service_years = diff.years
        else:
            self.service_years = 0

    @api.onchange('no_months', 'employee_id')
    def onchange_no_months(self):
        self.ensure_one()
        self.loan_amount = self.no_months * self.salary
    
    def _compute_end_payment_date(self):
        if(self.loan_lines):
            date = max(self.loan_lines.mapped('date'))
            self.end_payment_date = date
        else:
            self.end_payment_date = False

    def _compute_monthly_payment(self):
        self.monthly_payment = self.loan_amount / self.installment