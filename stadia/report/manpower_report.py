import math
from odoo import api, fields, models
from datetime import datetime

class ManpowerReport(models.AbstractModel):
    _name = 'report.stadia.hired_manpower_report'
    _inherit = 'report.report_xlsx.abstract'
    
    @api.model
    def get_html(self, date_from, date_to):
        data = self._get_report_data(date_from, date_to)
        return self.env.ref('stadia.manpower_report_template')._render(data)

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet()

        # Set up some formats to use.
        bold = workbook.add_format({'bold': True})

        start_date = data['form']['date_from']
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = data['form']['date_to']
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        header_format = workbook.add_format()
        header_format.set_font_size(15)
        header_format.set_bold()
        header_format.set_align('center')
        header_format.set_align('vcenter')
        header_format.set_border(style=1)
        date_format = workbook.add_format()
        date_format.set_font_size(10)
        date_format.set_bold()
        date_format.set_align('center')
        date_format.set_align('vcenter')
        date_format.set_border(style=1)

        max_col = 9
        left_cols = math.floor(max_col * 0.25)
        center_cols = math.ceil(max_col * 0.5)
        right_cols = math.floor(max_col * 0.25)

        sheet.merge_range(0, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(1, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(2, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(0, left_cols, 0, max_col, 'ስታድያ የምህንድስና ስራዎች ኃላ/የተ/የግ/ማህበር', header_format)
        sheet.merge_range(1, left_cols, 1, max_col, 'STADIA Engineering Works Consultant PLC', header_format)
        sheet.merge_range(2, left_cols, 2, max_col - right_cols, 'Report', header_format)
        sheet.set_row(2, 50)
        sheet.merge_range(2, max_col - right_cols + 1, 2, max_col, 'Date 111 - 2222', date_format)

        start_row = 3
        # Get the employees from contract id

        employees = self.sudo().env['hr.employee'].search([('contract_id', '!=', False)])



        sheet.write(start_row, 0, 'Name of Employe', bold)
        sheet.write(start_row, 1, 'Position', bold)
        sheet.write(start_row, 2, 'Basic Salary', bold)
        sheet.write(start_row, 3, 'Perdime', bold)
        sheet.write(start_row, 4, 'Desert Allowance', bold)
        sheet.write(start_row, 5, 'Project', bold)
        sheet.write(start_row, 6, 'Date of Hired', bold)

        col = start_row + 1
        for employee in employees:             
            ## TODO: improve efficiency
            if(not employee.first_contract_date):
                continue

            if(employee.first_contract_date >= start_date and employee.first_contract_date <= end_date):
                sheet.write(col, 0, employee.name)
                sheet.write(col, 1, employee.job_id.name)
                sheet.write(col, 2, employee.contract_id.wage)
                sheet.write(col, 3, employee.contract_id.perdime)
                sheet.write(col, 4, '')
                sheet.write(col, 5, employee.contract_id.work_place_id.name)
                sheet.write(col, 6, employee.first_contract_date.strftime('%m/%d/%Y'))
                col += 1

class LateralTransferManpowerReport(models.AbstractModel):
    _name = 'report.stadia.lateral_transfer_manpower_report'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet()

        # Set up some formats to use.
        bold = workbook.add_format({'bold': True})

        start_date = data['form']['date_from']
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = data['form']['date_to']
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # i.e contract signed stage
        last_stage_id = self.env['stadia.promotion.stage'].search([])
        last_stage_id = max(last_stage_id.mapped('sequence'))
        promotions = self.env['stadia.promotion'].search([('stage_id', '=', last_stage_id), ('promotion_type', '=', 'transfer')])

        sheet.write(0, 0, 'Name of Employe', bold)
        sheet.write(0, 1, 'Position', bold)
        sheet.write(0, 2, 'Basic Salary', bold)
        sheet.write(0, 3, 'Perdime', bold)
        sheet.write(0, 4, 'Desert Allowance', bold)
        sheet.write(0, 5, 'Transfer From', bold)
        sheet.write(0, 6, 'Transfer To', bold)
        sheet.write(0, 7, 'Transfer Date', bold)

        col = 1
        for promotion in promotions:
            # Check the employee has signed a contract
            contract_count = self.env['hr.contract'].search_count([('employee_id', '=', promotion.employee_id.id), ('date_start', '>=', promotion.start_date), ('state', '=', 'open')])
            sheet.write(col, 0, promotion.employee_id.name)
            sheet.write(col, 1, promotion.employee_id.job_id.name)
            sheet.write(col, 2, promotion.employee_id.contract_id.wage)
            sheet.write(col, 3, promotion.employee_id.contract_id.perdime)
            sheet.write(col, 4, '')
            sheet.write(col, 4, '')
            sheet.write(col, 4, promotion.new_work_place.name)
            sheet.write(col, 4, promotion.start_date)
            col += 1

class PromotionManpowerReport(models.AbstractModel):
    _name = 'report.stadia.promotion_manpower_report'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet()

        # Set up some formats to use.
        bold = workbook.add_format({'bold': True})

        start_date = data['form']['date_from']
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = data['form']['date_to']
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        # i.e contract signed stage
        last_stage_id = self.env['stadia.promotion.stage'].search([])
        last_stage_id = max(last_stage_id.mapped('sequence'))
        promotions = self.env['stadia.promotion'].search([('stage_id', '=', last_stage_id), ('promotion_type', '=', 'promotion')])

        sheet.write(0, 0, 'Name of Employe', bold)
        sheet.write(0, 1, 'Position', bold)
        sheet.write(0, 2, 'Basic Salary', bold)
        sheet.write(0, 3, 'Perdime', bold)
        sheet.write(0, 4, 'Desert Allowance', bold)
        sheet.write(0, 5, 'Transfer From', bold)
        sheet.write(0, 6, 'Transfer To', bold)
        sheet.write(0, 7, 'Transfer Date', bold)

        col = 1
        for promotion in promotions:
            # Check the employee has signed a contract
            contract_count = self.env['hr.contract'].search_count([('employee_id', '=', promotion.employee_id.id), ('date_start', '>=', promotion.start_date), ('state', '=', 'open')])
            sheet.write(col, 0, promotion.employee_id.name)
            sheet.write(col, 1, promotion.employee_id.job_id.name)
            sheet.write(col, 2, promotion.employee_id.contract_id.wage)
            sheet.write(col, 3, promotion.employee_id.contract_id.perdime)
            sheet.write(col, 4, '')
            sheet.write(col, 4, '')
            sheet.write(col, 4, promotion.new_work_place.name)
            sheet.write(col, 4, promotion.start_date)
            col += 1