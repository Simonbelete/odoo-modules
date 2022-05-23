from odoo import fields, api, models

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    mrp_production_salary = fields.Float(compute="_compute_mrp_production_salary")

    def _compute_mrp_production_salary(self):
        print("888888888888888888888888888888888888888")
        print("888888888888888888888888888888888888888")
        for record in self:
            t_sal = 0
            # mrp_salary = self.env['mrp.production'].search([
            #     ('employee_id', '=', record.employee_id.id),
            #     ('state', '=', 'done')
            #     ])
            # for s in mrp_salary:
            #     for m in s.move_finished_ids:
            #         t_sal = t_sal + (s.salary * s.product_qty)

            record.mrp_production_salary = t_sal