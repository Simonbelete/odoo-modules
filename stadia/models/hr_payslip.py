from odoo import fields, api, models, tools, _

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    tax_dec = fields.Float(compute="_compute_tax_dec")
    # untaken_leave_salary = fields.Float(default=0, compute="_compute_untaken_leave")
    remaining_leaves = fields.Float(related='employee_id.remaining_leaves')

    def _compute_tax_dec(self):
        for total_wage in self:
            if total_wage.contract_id.wage >= 0 and total_wage.contract_id.wage <= 600:
                total_wage.tax_dec = 0
            elif total_wage.contract_id.wage > 600 and total_wage.contract_id.wage <= 1650:
                total_wage.tax_dec = total_wage.contract_id.wage * 0.1
            elif total_wage.contract_id.wage > 1650 and total_wage.contract_id.wage <= 3200:
                total_wage.tax_dec = total_wage.contract_id.wage * 0.15
            elif total_wage.contract_id.wage > 3200 and total_wage.contract_id.wage <= 5250:
                total_wage.tax_dec = total_wage.contract_id.wage * 0.2
            elif total_wage.contract_id.wage > 5250 and total_wage.contract_id.wage <= 7800:
                total_wage.tax_dec = total_wage.contract_id.wage * 0.25
            elif total_wage.contract_id.wage > 7800 and total_wage.contract_id.wage <= 10900:
                total_wage.tax_dec = total_wage.contract_id.wage * 0.3
            elif total_wage.contract_id.wage > 10900:
                total_wage.tax_dec = total_wage.contract_id.wage * 0.35

    # def _compute_untaken_leave(self):
    #     leave_allocation = self.env['hr.leave.allocation'].search([
    #         ('employee_id', '=', self.employee_id.id)
    #     ])
        
    #     print("--------ssss-------------------------------")
    #     print(leave_allocation)
    #     print(self.employee_id.remaining_leaves)
    #     print("---------sss------------------------------")
    #     if(leave_allocation):
    #         self.untaken_leave_salary = self.contract_id.wage/208 * self.employee_id.remaining_leaves
    #     else:
    #         self.untaken_leave_salary = 0
