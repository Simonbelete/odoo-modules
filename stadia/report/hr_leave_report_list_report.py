from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime

class HrLeaveReportListReport(models.AbstractModel):
    _name = 'report.stadia.leave_report'
    _inherit = 'report.report_xlsx.abstract'

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        return {

        }

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        
        leave_report = []
        employee_ids = data['form']['emp']
        date_to =  datetime.now()

        print('11111111111111111122222222222222')
        print(employee_ids)
        
        ## Select leave types i.e years from data.date_to
        ## and sor them by end or start date
        time_off_types = self.env['hr.leave.type'].search([])

        # Headers
        row = 0
        sheet.write(0, row, 'Name of Employee', bold)
        sheet.set_column(0, row, 50)
        row += 1
        sheet.write(0, row, 'Department', bold)
        sheet.set_column(0, row, 50)
        row += 1
        sheet.write(0, row, 'Project', bold)
        sheet.set_column(0, row, 50)
        row += 1
        sheet.write(0, row, 'Position', bold)
        sheet.set_column(0, row, 50)
        row += 1
        sheet.write(0, row, 'Date of Employeement', bold)
        sheet.set_column(0, row, 50)
        row += 1
        sheet.write(0, row, 'End date', bold)
        sheet.set_column(0, row, 50)

        for time_off_type in time_off_types:
            sheet.write(0, row, time_off_type.name, bold)
            row += 1

        row += 1
        sheet.write(0, row, 'Total used in the year', bold)
        sheet.set_column(0, row, 50)

        row += 1
        sheet.write(0, row, 'Annual Leave balance', bold)
        sheet.set_column(0, row, 50)

        col = 1
        row = 0
        for emp_id in employee_ids:
            employee = self.env['hr.employee'].search([('id', '=', emp_id)])
            sheet.write(col, 0, employee.name)
            sheet.write(col, 1, employee.department_id.name)
            sheet.write(col, 2, employee.contract_id.work_place_id.name)
            sheet.write(col, 3, employee.job_id.name)
            sheet.write(col, 4, employee.first_contract_date)
            sheet.write(col, 5, date_to)

            sheet.set_h_pagebreaks([10])
            # vals = {
            #     'employee': employee,
            # }
            # sheet.write(j, 0, employee.name)
            # i = 0
            # for time_off_type in time_off_types:
            #     self.env.cr.execute(
            #         """
            #         SELECT SUM(allocation.holiday_status_id)
            #             FROM hr_leave_allocation as allocation
            #             WHERE 
            #                 allocation.employee_id = %s
            #                 holiday_status_id %s
            #         """ % (employee.id, time_off_type.id)
            #     )
            #     sum_time_off_type = self.env.cr.fetchall()
            #     vals[time_off_type.id] = time_off_type
            #     vals[time_off_type.id]['total'] = sum_time_off_type
            #     sheet.write(j, i, sum_time_off_type)
            #     i += 1

            # leave_report.append(vals)
            col +=1

