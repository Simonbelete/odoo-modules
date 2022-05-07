from odoo import tools, api
from odoo import models, fields


class SummaryView(models.Model):
    _name = 'summary.report'
    _auto = False
    _description = 'Summary report'

    parent_id = fields.Many2one('hr.employee')
    pension_d = fields.Integer()
    medical_insurance = fields.Integer(string='Medical Insurance')
    name = fields.Char()

    def init(self):
        tools.drop_view_if_exists(self._cr, 'summary_report')
        self._cr.execute("""
        CREATE OR REPLACE VIEW summary_report AS (
         SELECT hr_contract.pension_d, hr_contract.medical_insurance, hr_employee.name
           FROM hr_contract
           INNER JOIN hr_employee ON hr_contract.employee_id=hr_employee.id
            
        )""")
