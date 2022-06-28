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

        # Set up some formats to use.
        bold = workbook.add_format({'bold': True})
        italic = workbook.add_format({'italic': True})
        red = workbook.add_format({'color': 'red'})
        blue = workbook.add_format({'color': 'blue'})
        center = workbook.add_format({'align': 'center'})
        superscript = workbook.add_format({'font_script': 1})

        employee_ids = data['form']['emp']
        date_to =  data['form']['date_to']
        date_max = datetime.strptime(date_to, '%Y-%m-%d')
        
        ## Select leave types i.e years from data.date_to
        ## and sor them by end or start date ('validity_stop')
        time_off_types = self.env['hr.leave.type'].search([('validity_stop', '<=', date_max)])

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
        sheet.set_column(0, row, 30)
        row += 1
        sheet.write(0, row, 'End date', bold)
        sheet.set_column(0, row, 30)

        for time_off_type in time_off_types:
            row += 1
            sheet.write(0, row, time_off_type.name, bold)

        row += 1
        total_annual_leave_row = row
        sheet.write(0, row, 'Total Annual Leave', bold)
        sheet.set_column(0, row, 20)

        row += 1
        total_used_row = row
        sheet.write(0, row, 'Total used in the year', bold)
        sheet.set_column(0, row, 20)

        row += 1
        annual_leave_balance_row = row
        sheet.write(0, row, 'Annual Leave balance', bold)
        sheet.set_column(0, row, 20)

        col = 1
        row = 0
        for emp_id in employee_ids:
            total_annual_leave = 0
            total_used_in_this_year = 0
            annual_leave_balance = 0
            employee = self.env['hr.employee'].search([('id', '=', emp_id)])
            sheet.write(col, 0, employee.name)
            sheet.write(col, 1, employee.department_id.name)
            sheet.write(col, 2, employee.contract_id.work_place_id.name)
            sheet.write(col, 3, employee.job_id.name)
            if(employee.first_contract_date):
                sheet.write(col, 4, employee.first_contract_date.strftime('%m/%d/%Y'))
            else:
                sheet.write(col, 4, '', red)

            sheet.write(col, 5, date_to)

            row_t = 6
            for time_off_type in time_off_types:
                # Get the current users total time off
                self.env.cr.execute(
                    """
                    SELECT SUM(allocation.number_of_days) AS total_time_off
                        FROM hr_leave_allocation as allocation
                        WHERE
                            allocation.employee_id = '%s'
                            AND
                            allocation.holiday_status_id = '%s'
                    """ % (employee.id, time_off_type.id)
                )
                sum_time_off_type = self.env.cr.fetchall()

                # Get the taken leaves
                self.env.cr.execute(
                    """
                    SELECT SUM(leaves.number_of_days)
                        FROM hr_leave as leaves
                         WHERE
                            leaves.employee_id = '%s'
                            AND
                            leaves.holiday_status_id = '%s'
                    """ % (employee.id, time_off_type.id)
                )
                sum_taken_leaves = self.env.cr.fetchall()

                # Check leaves
                sum_time_off_type = sum_time_off_type[0][0] if sum_time_off_type[0][0] else 0
                sum_taken_leaves = sum_taken_leaves[0][0] if sum_taken_leaves[0][0] else 0

                remaining_leaves = sum_time_off_type - sum_taken_leaves
                total_annual_leave += remaining_leaves
                annual_leave_balance = total_annual_leave
                sheet.write(col, row_t, remaining_leaves)
                row_t += 1

            sheet.write(col, total_annual_leave_row, total_annual_leave)
            sheet.write(col, total_used_row, total_used_in_this_year)
            sheet.write(col, annual_leave_balance_row, annual_leave_balance)
            # sheet.set_h_pagebreaks([10])
            col +=1

