import babel
from datetime import date, time, datetime
from pytz import timezone
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
                total_wage.tax_dec = total_wage.contract_id.wage * 0.1 - 60
            elif total_wage.contract_id.wage > 1650 and total_wage.contract_id.wage <= 3200:
                total_wage.tax_dec = total_wage.contract_id.wage * 0.15 - 142.5
            elif total_wage.contract_id.wage > 3200 and total_wage.contract_id.wage <= 5250:
                total_wage.tax_dec = total_wage.contract_id.wage * 0.2 - 302.5
            elif total_wage.contract_id.wage > 5250 and total_wage.contract_id.wage <= 7800:
                total_wage.tax_dec = total_wage.contract_id.wage * 0.25 - 565
            elif total_wage.contract_id.wage > 7800 and total_wage.contract_id.wage <= 10900:
                total_wage.tax_dec = total_wage.contract_id.wage * 0.3 - 955
            elif total_wage.contract_id.wage > 10900:
                total_wage.tax_dec = total_wage.contract_id.wage * 0.35 - 1500

    @api.model
    def get_worked_day_lines(self, contracts, date_from, date_to, attendances_lists):
        """
        @param contract: Browse record of contracts
        @return: returns a list of dict containing the input that should be applied for the given contract between date_from and date_to
        """
        res = []
        # fill only if the contract as a working schedule linked
        for contract in contracts.filtered(lambda contract: contract.resource_calendar_id):
            day_from = datetime.combine(fields.Date.from_string(date_from), time.min)
            day_to = datetime.combine(fields.Date.from_string(date_to), time.max)

            # compute leave days
            leaves = {}
            calendar = contract.resource_calendar_id
            tz = timezone(calendar.tz)
            day_leave_intervals = contract.employee_id.list_leaves(day_from, day_to, calendar=contract.resource_calendar_id)
            for day, hours, leave in day_leave_intervals:
                holiday = leave.holiday_id
                current_leave_struct = leaves.setdefault(holiday.holiday_status_id, {
                    'name': holiday.holiday_status_id.name or _('Global Leaves'),
                    'sequence': 5,
                    'code': holiday.holiday_status_id.code or 'GLOBAL',
                    'number_of_days': 0.0,
                    'number_of_hours': 0.0,
                    'contract_id': contract.id,
                })
                current_leave_struct['number_of_hours'] += hours
                work_hours = calendar.get_work_hours_count(
                    tz.localize(datetime.combine(day, time.min)),
                    tz.localize(datetime.combine(day, time.max)),
                    compute_leaves=False,
                )
                if work_hours:
                    current_leave_struct['number_of_days'] += hours / work_hours

            # compute worked days
            work_data = contract.employee_id._get_work_days_data(day_from, day_to, calendar=contract.resource_calendar_id)
            attendances = {
                'name': _("Normal Working Days paid at 100%"),
                'sequence': 1,
                'code': 'WORK100',
                'number_of_days': work_data['days'],
                'number_of_hours': work_data['hours'],
                'contract_id': contract.id,
            }

            worked_attendances = {
                'name': 'Attendances Working Days',
                'code': 'ATT',
                'number_of_days': 0,
                'number_of_hours': 0,
                'contract_id': contract.id
            }
            # Tab in Tab out attendace
            if attendances_lists:
                worked_hours = 0
                # Loop through attendance and add the worked_hours
                for attendance in attendances_lists:
                    worked_hours = worked_hours + attendance.worked_hours

                # Take out lunch time per day
                total_lunch_time = worked_hours/8 # 8 hr (1day)
                worked_hours = worked_hours - total_lunch_time 
                worked_attendances['number_of_days'] = worked_hours/24
                worked_attendances['number_of_hours'] = worked_hours

            perdime_worked_days = {
                'name': 'Per dime Working Days',
                'code': 'PD',
                'number_of_days': work_data['days'],
                'number_of_hours': work_data['hours'],
                'contract_id': contract.id
            }

            res.append(attendances)
            res.append(worked_attendances)
            res.append(perdime_worked_days)
            res.extend(leaves.values())
        return res


    @api.onchange('employee_id', 'date_from', 'date_to')
    def onchange_employee(self):
        self.ensure_one()
        if (not self.employee_id) or (not self.date_from) or (not self.date_to):
            return
        employee = self.employee_id
        date_from = self.date_from
        date_to = self.date_to
        contract_ids = []

        ttyme = datetime.combine(fields.Date.from_string(date_from), time.min)
        locale = self.env.context.get('lang') or 'en_US'
        self.name = _('Salary Slip of %s for %s') % (employee.name, tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM-y', locale=locale)))
        self.company_id = employee.company_id

        if not self.env.context.get('contract') or not self.contract_id:
            contract_ids = self.get_contract(employee, date_from, date_to)
            if not contract_ids:
                return
            self.contract_id = self.env['hr.contract'].browse(contract_ids[0])

        if not self.contract_id.struct_id:
            return
        self.struct_id = self.contract_id.struct_id

        #computation of the salary input
        contracts = self.env['hr.contract'].browse(contract_ids)
        if contracts:
            start_date = datetime.combine(date_from, time.min)
            end_date = datetime.combine(date_to, time.max)
            attendances = self.env['hr.attendance'].search([
                ('employee_id', '=', self.employee_id.id),
                ('check_in', '>=', start_date),
                ('check_out', '<=', end_date)
            ])
            worked_days_line_ids = self.get_worked_day_lines(contracts, date_from, date_to, attendances)
            worked_days_lines = self.worked_days_line_ids.browse([])
            for r in worked_days_line_ids:
                worked_days_lines += worked_days_lines.new(r)
            self.worked_days_line_ids = worked_days_lines

            input_line_ids = self.get_inputs(contracts, date_from, date_to)
            input_lines = self.input_line_ids.browse([])
            for r in input_line_ids:
                input_lines += input_lines.new(r)
            self.input_line_ids = input_lines
            return