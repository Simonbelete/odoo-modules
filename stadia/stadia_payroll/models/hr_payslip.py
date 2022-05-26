from datetime import date, time, datetime
from odoo import fields, api, models

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.onchange('employee_id', 'date_from', 'date_to')
    def onchange_pyaslip_data(self):
        """ When the above data changes calculate attendance hours 
            and save the hours in hr.payslip.worked_days for further calculation
            on salary rule   hours
        """
        for record in self:
            start_date = datetime.combine(record.date_from, time.min)
            end_date = datetime.combine(record.date_to, time.max)
            attendances = self.env['hr.attendance'].search([
                ('employee_id', '=', record.employee_id.id),
                ('check_in', '>=', start_date),
                ('check_out', '<=', end_date)
            ])

            print('-----------------------------')
            print(start_date)
            print(end_date)
            print(attendances)
            print('------------------------------------')
            if attendances:
                worked_hours = 0
                # Loop through attendance and add the worked_hours
                for attendance in attendances:
                    worked_hours = worked_hours + attendance.worked_hours

                # Add the worked hours to the lines id with code
                self.env['hr.payslip.worked_days'].create({
                    'name': 'Attendances Working Days',
                    'payslip_id': self._origin.id,
                    'code': 'ATT',
                    'number_of_days': worked_hours/24,
                    'number_of_hours': worked_hours,
                    'contract_id': record.contract_id.id
                })