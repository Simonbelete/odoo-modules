import math
import os
from odoo import api, fields, models
from datetime import datetime

class AllManpowerReport(models.AbstractModel):
    _name = 'report.stadia.all_manpower_report'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet()

        # Set up some formats to use.
        bold = workbook.add_format({'bold': True})
        bold.set_border(style=1)

        start_date = data['form']['date_from']
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = data['form']['date_to']
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        border = workbook.add_format()
        border.set_border(style=1)
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
        max_row = 3
        left_cols = math.floor(max_col * 0.25)
        center_cols = math.ceil(max_col * 0.5)
        right_cols = math.floor(max_col * 0.25)

        dir_path = os.path.dirname(os.path.realpath(__file__))

        sheet.merge_range(0, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(1, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(2, 0, 0, left_cols - 1, '', header_format)
        sheet.insert_image(0, 0, '%s/stadia_plain_logo.png' % dir_path, {'x_scale': 0.6, 'y_scale': 0.4})
        sheet.merge_range(0, left_cols, 0, max_col, 'ስታድያ የምህንድስና ስራዎች ኃላ/የተ/የግ/ማህበር', header_format)
        sheet.merge_range(1, left_cols, 1, max_col, 'STADIA Engineering Works Consultant PLC', header_format)
        sheet.merge_range(2, left_cols, 2, max_col - right_cols, 'EMPLOYMENT, TRANSFER, TERMINATION REPORT', header_format)
        sheet.set_row(2, 50)
        sheet.merge_range(2, max_col - right_cols + 1, 2, max_col, 'Date:- %s - %s' % (start_date.strftime('%m/%d/%Y'), end_date.strftime('%m/%d/%Y')), date_format)

        # Get the employees from contract id
        employees = self.sudo().env['hr.employee'].search([('contract_id', '!=', False)])

        sheet.write(max_row + 1, 0, 'No', bold)
        sheet.write(max_row + 1, 1, 'Name of Employee', bold)
        sheet.write(max_row + 1, 2, 'Position', bold)
        sheet.write(max_row + 1, 3, 'Basic Salary', bold)
        sheet.write(max_row + 1, 4, 'Perdime', bold)
        sheet.write(max_row + 1, 5, 'Desert Allowance', bold)
        sheet.write(max_row + 1, 6, 'Project', bold)
        sheet.write(max_row + 1, 7, 'Date of Hired', bold)

        # Sizes
        sheet.set_column(0, 0,  5)
        sheet.set_column(1, 1, 30)
        sheet.set_column(2, 2, 20)
        sheet.set_column(3, 3, 20)
        sheet.set_column(4, 4, 20)
        sheet.set_column(5, 5, 20)
        sheet.set_column(6, 6, 20)
        sheet.set_column(7, 7, 20)
        sheet.set_column(8, 8, 20)

        row = max_row + 2
        c = 1
        for employee in employees:             
            ## TODO: improve efficiency
            if(not employee.first_contract_date):
                continue

            if(employee.first_contract_date >= start_date and employee.first_contract_date <= end_date):
                sheet.write(row, 0, c, border)
                sheet.write(row, 1, employee.name, border)
                sheet.write(row, 2, employee.job_id.name, border)
                sheet.write(row, 3, employee.contract_id.wage, border)
                sheet.write(row, 4, employee.contract_id.perdime, border)
                sheet.write(row, 5, '', border)
                sheet.write(row, 6, employee.contract_id.work_place_id.name, border)
                sheet.write(row, 7, employee.first_contract_date.strftime('%m/%d/%Y'), border)
                row += 1
                c += 1

        ####################################
        ## Lateral Transfer
        ####################################

        # i.e contract signed stage
        last_stage_id = self.env['stadia.promotion.stage'].search([])
        last_stage_id = max(last_stage_id.mapped('sequence'))
        lateral_transfer = self.env['stadia.promotion'].search([('stage_id', '=', last_stage_id), ('promotion_type', '=', 'transfer')])

        row += 1
        sheet.write(row, 0, 'Lateral Transfer')
        row += 1
        sheet.write(row, 0, 'No', bold)
        sheet.write(row, 1, 'Name of Employe', bold)
        sheet.write(row, 2, 'Position', bold)
        sheet.write(row, 3, 'Basic Salary', bold)
        sheet.write(row, 4, 'Perdime', bold)
        sheet.write(row, 5, 'Desert Allowance', bold)
        sheet.write(row, 6, 'Transfer From', bold)
        sheet.write(row, 7, 'Transfer To', bold)
        sheet.write(row, 8, 'Transfer Date', bold)


        row = row + 1
        c = 1
        for transfer in lateral_transfer:
            # Check the employee has signed a contract
            contract_count = self.env['hr.contract'].search_count([('employee_id', '=', transfer.employee_id.id), ('date_start', '=', transfer.start_date), ('state', '=', 'open')])
            style = border
            if(contract_count == 0):
                style = workbook.add_format()
                style.set_border(style=1)
                style.set_bg_color('#66666')
            sheet.write(row, 0, c, style)
            sheet.write(row, 1, transfer.employee_id.name, style)
            sheet.write(row, 2, transfer.employee_id.job_id.name, style)
            sheet.write(row, 3, transfer.salary, style)
            sheet.write(row, 4, transfer.perdime, style)
            sheet.write(row, 5, '', style)
            sheet.write(row, 6, transfer.active_work_place_id.name if transfer.active_work_place_id else '', style)
            sheet.write(row, 7, transfer.new_work_place.name, style)
            sheet.write(row, 8, transfer.start_date.strftime('%m/%d/%Y'), style)
            row += 1
            c += 1

        ####################################
        ## Promtion
        ####################################
        row += 1
        sheet.merge_range(row, 0, row, max_col -1, 'Promotion', border)
        
        promotions = self.env['stadia.promotion'].search([('stage_id', '=', last_stage_id), ('promotion_type', '=', 'promotion')])

        row = row + 1
        c = 1
        for promotion in promotions:
            # Check the employee has signed a contract
            contract_count = self.env['hr.contract'].search_count([('employee_id', '=', promotion.employee_id.id), ('date_start', '=', promotion.start_date), ('state', '=', 'open')])
            style = border
            if(contract_count == 0):
                style = workbook.add_format()
                style.set_border(style=1)
                style.set_bg_color('#66666')
            sheet.write(row, 0, c, style)
            sheet.write(row, 1, promotion.employee_id.name, style)
            sheet.write(row, 2, promotion.employee_id.job_id.name, style)
            sheet.write(row, 3, promotion.salary, style)
            sheet.write(row, 4, promotion.perdime, style)
            sheet.write(row, 5, '', style)
            sheet.write(row, 6, promotion.active_work_place_id.name if promotion.active_work_place_id else '', style)
            sheet.write(row, 7, promotion.new_work_place.name, style)
            sheet.write(row, 8, promotion.start_date.strftime('%m/%d/%Y'), style)
            row += 1
            c += 1

        ####################################
        ## Active False
        ####################################
        row += 1
        sheet.merge_range(row, 0, row, max_col -1, 'Termination', border)
        
        employees = self.sudo().env['hr.employee'].search([
            ('active', '=', False),
            ('departure_date', '>=', start_date),
            ('departure_date', '<=', end_date)
        ])

        row = row + 1
        c = 1
        for promotion in employees:
            sheet.write(row, 0, c, border)
            sheet.write(row, 1, employee.name, border)
            sheet.write(row, 2, '', border)
            # sheet.write(row, 2, employee.job_id.name, border)
            sheet.write(row, 3, employee.contract_id.wage, border)
            # sheet.write(row, 4, employee.contract_id.perdime, border)
            sheet.write(row, 4, '', border)
            sheet.write(row, 5, '', border)
            # sheet.write(row, 6, employee.contract_id.work_place_id.name, border)
            sheet.write(row, 6, '', border)
            if(employee.departure_date):
                sheet.write(row, 7, employee.departure_date.strftime('%m/%d/%Y'), border)
            else:
                sheet.write(row, 7, '', border)
            row += 1
            c += 1

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
        max_row = 3
        left_cols = math.floor(max_col * 0.25)
        center_cols = math.ceil(max_col * 0.5)
        right_cols = math.floor(max_col * 0.25)

        dir_path = os.path.dirname(os.path.realpath(__file__))

        sheet.merge_range(0, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(1, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(2, 0, 0, left_cols - 1, '', header_format)
        sheet.insert_image(0, 0, '%s/stadia_plain_logo.png' % dir_path, {'x_scale': 0.6, 'y_scale': 0.4})
        sheet.merge_range(0, left_cols, 0, max_col, 'ስታድያ የምህንድስና ስራዎች ኃላ/የተ/የግ/ማህበር', header_format)
        sheet.merge_range(1, left_cols, 1, max_col, 'STADIA Engineering Works Consultant PLC', header_format)
        sheet.merge_range(2, left_cols, 2, max_col - right_cols, 'Report', header_format)
        sheet.set_row(2, 50)
        sheet.merge_range(2, max_col - right_cols + 1, 2, max_col, 'Date 111 - 2222', date_format)

        # Get the employees from contract id
        employees = self.sudo().env['hr.employee'].search([('contract_id', '!=', False)])

        sheet.write(max_row + 1, 0, 'No', bold)
        sheet.write(max_row + 1, 1, 'Name of Employe', bold)
        sheet.write(max_row + 1, 2, 'Position', bold)
        sheet.write(max_row + 1, 3, 'Basic Salary', bold)
        sheet.write(max_row + 1, 4, 'Perdime', bold)
        sheet.write(max_row + 1, 5, 'Desert Allowance', bold)
        sheet.write(max_row + 1, 6, 'Project', bold)
        sheet.write(max_row + 1, 7, 'Date of Hired', bold)

        # Sizes
        sheet.set_column(0, 0,  5)
        sheet.set_column(1, 1, 30)
        sheet.set_column(2, 2, 20)
        sheet.set_column(3, 3, 20)
        sheet.set_column(4, 4, 20)
        sheet.set_column(5, 5, 20)
        sheet.set_column(6, 6, 20)
        sheet.set_column(7, 7, 20)

        col = max_row + 2
        for employee in employees:             
            ## TODO: improve efficiency
            if(not employee.first_contract_date):
                continue

            if(employee.first_contract_date >= start_date and employee.first_contract_date <= end_date):
                sheet.write(col, 0, col - max_row - 1)
                sheet.write(col, 1, employee.name)
                sheet.write(col, 2, employee.job_id.name)
                sheet.write(col, 3, employee.contract_id.wage)
                sheet.write(col, 4, employee.contract_id.perdime)
                sheet.write(col, 5, '')
                sheet.write(col, 6, employee.contract_id.work_place_id.name)
                sheet.write(col, 7, employee.first_contract_date.strftime('%m/%d/%Y'))
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
        max_row = 3
        left_cols = math.floor(max_col * 0.25)
        center_cols = math.ceil(max_col * 0.5)
        right_cols = math.floor(max_col * 0.25)

        dir_path = os.path.dirname(os.path.realpath(__file__))

        sheet.merge_range(0, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(1, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(2, 0, 0, left_cols - 1, '', header_format)
        sheet.insert_image(0, 0, '%s/stadia_plain_logo.png' % dir_path, {'x_scale': 0.6, 'y_scale': 0.4})
        sheet.merge_range(0, left_cols, 0, max_col, 'ስታድያ የምህንድስና ስራዎች ኃላ/የተ/የግ/ማህበር', header_format)
        sheet.merge_range(1, left_cols, 1, max_col, 'STADIA Engineering Works Consultant PLC', header_format)
        sheet.merge_range(2, left_cols, 2, max_col - right_cols, 'Report', header_format)
        sheet.set_row(2, 50)
        sheet.merge_range(2, max_col - right_cols + 1, 2, max_col, 'Date:- %s - %s' % (start_date.strftime('%m/%d/%Y'), end_date.strftime('%m/%d/%Y')), date_format)

        # i.e contract signed stage
        last_stage_id = self.env['stadia.promotion.stage'].search([])
        last_stage_id = max(last_stage_id.mapped('sequence'))
        promotions = self.env['stadia.promotion'].search([
            ('stage_id', '=', last_stage_id), 
            ('promotion_type', '=', 'transfer'),
            ('start_date', '>=', start_date),
            ('start_date', '<=', end_date),
            ])

        sheet.write(max_row + 1, 0, 'Name of Employe', bold)
        sheet.write(max_row + 1, 1, 'Position', bold)
        sheet.write(max_row + 1, 2, 'Basic Salary', bold)
        sheet.write(max_row + 1, 3, 'Perdime', bold)
        sheet.write(max_row + 1, 4, 'Desert Allowance', bold)
        sheet.write(max_row + 1, 5, 'Transfer From', bold)
        sheet.write(max_row + 1, 6, 'Transfer To', bold)
        sheet.write(max_row + 1, 7, 'Transfer Date', bold)

        # Sizes
        sheet.set_column(0, 0,  5)
        sheet.set_column(1, 1, 30)
        sheet.set_column(2, 2, 20)
        sheet.set_column(3, 3, 20)
        sheet.set_column(4, 4, 20)
        sheet.set_column(5, 5, 20)
        sheet.set_column(6, 6, 20)
        sheet.set_column(7, 7, 20)

        col = max_row + 2
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
        max_row = 3
        left_cols = math.floor(max_col * 0.25)
        center_cols = math.ceil(max_col * 0.5)
        right_cols = math.floor(max_col * 0.25)

        dir_path = os.path.dirname(os.path.realpath(__file__))

        sheet.merge_range(0, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(1, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(2, 0, 0, left_cols - 1, '', header_format)
        sheet.insert_image(0, 0, '%s/stadia_plain_logo.png' % dir_path, {'x_scale': 0.6, 'y_scale': 0.4})
        sheet.merge_range(0, left_cols, 0, max_col, 'ስታድያ የምህንድስና ስራዎች ኃላ/የተ/የግ/ማህበር', header_format)
        sheet.merge_range(1, left_cols, 1, max_col, 'STADIA Engineering Works Consultant PLC', header_format)
        sheet.merge_range(2, left_cols, 2, max_col - right_cols, 'Report', header_format)
        sheet.set_row(2, 50)
        sheet.merge_range(2, max_col - right_cols + 1, 2, max_col, 'Date:- %s - %s' % (start_date.strftime('%m/%d/%Y'), end_date.strftime('%m/%d/%Y')), date_format)


        # i.e contract signed stage
        last_stage_id = self.env['stadia.promotion.stage'].search([])
        last_stage_id = max(last_stage_id.mapped('sequence'))
        promotions = self.env['stadia.promotion'].search([('stage_id', '=', last_stage_id), ('promotion_type', '=', 'promotion')])

        sheet.write(max_row + 1, 0, 'Name of Employe', bold)
        sheet.write(max_row + 1, 1, 'Position', bold)
        sheet.write(max_row + 1, 2, 'Basic Salary', bold)
        sheet.write(max_row + 1, 3, 'Perdime', bold)
        sheet.write(max_row + 1, 4, 'Desert Allowance', bold)
        sheet.write(max_row + 1, 5, 'Transfer From', bold)
        sheet.write(max_row + 1, 6, 'Transfer To', bold)
        sheet.write(max_row + 1, 7, 'Transfer Date', bold)

        sheet.set_column(0, 0,  5)
        sheet.set_column(1, 1, 30)
        sheet.set_column(2, 2, 20)
        sheet.set_column(3, 3, 20)
        sheet.set_column(4, 4, 20)
        sheet.set_column(5, 5, 20)
        sheet.set_column(6, 6, 20)
        sheet.set_column(7, 7, 20)

        col = max_row + 2
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