import xlsxwriter
import math
from datetime import datetime
from odoo import api, models

class AssetMovementReport(models.AbstractModel):
    _name = 'report.stadia.asset_movement_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet()

        # Set up some formats to use.
        bold = workbook.add_format({'bold': True})

        start_date = data['form']['date_from']
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = data['form']['date_to']
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        bold = workbook.add_format({'bold': True})
        bold.set_border(style=1)
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
        assset_style = workbook.add_format({'bg_color': '#edeff1'})

        # Header
        max_col = 5
        max_row = 3
        left_cols = math.floor(max_col * 0.25)
        center_cols = math.ceil(max_col * 0.5)
        right_cols = math.floor(max_col * 0.25)

        sheet.merge_range(0, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(1, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(2, 0, 0, left_cols - 1, '', header_format)
        sheet.merge_range(0, left_cols, 0, max_col, 'ስታድያ የምህንድስና ስራዎች ኃላ/የተ/የግ/ማህበር', header_format)
        sheet.merge_range(1, left_cols, 1, max_col, 'STADIA Engineering Works Consultant PLC', header_format)
        sheet.merge_range(2, left_cols, 2, max_col - right_cols, 'EMPLOYMENT, TRANSFER, TERMINATION REPORT', header_format)
        sheet.set_row(2, 50)
        # sheet.merge_range(2, max_col - right_cols + 1, 2, max_col, 'Date:- %s - %s' % (start_date.strftime('%m/%d/%Y'), end_date.strftime('%m/%d/%Y')), date_format)
        sheet.write(2, max_col - right_cols + 1, 'Date:- %s - %s' % (start_date.strftime('%m/%d/%Y'), end_date.strftime('%m/%d/%Y')), date_format)

        sheet.write(max_row + 1, 0, 'No', bold)
        sheet.write(max_row + 1, 1, 'STA No', bold)
        # sheet.write(max_row + 1, 2, 'S/N', bold)
        sheet.write(max_row + 1, 2, 'Description/Item', bold)
        sheet.write(max_row + 1, 3, 'Location', bold)
        sheet.write(max_row + 1, 4, 'Employee', bold)

        # Sizes
        sheet.set_column(0, 0, 5)
        sheet.set_column(1, 1, 30)
        sheet.set_column(2, 2, 20)
        sheet.set_column(3, 3, 20)
        sheet.set_column(4, 4, 30)

        asset_ids = data['form']['asset']

        row = max_row + 2
        c = 1
        for asset_id in asset_ids:
            asset = self.env['stadia.asset'].search([('id', '=', asset_id)])
            movements = self.env['asset.movement'].search([
                ('asset_id', '=', asset_id)
                ('state', '=', 'approved'),
                ('date', '>=', start_date),
                ('date', '<=', end_date)
            ])
            sheet.write(row, 0, c, assset_style)
            sheet.write(row, 1, asset.id_t_no, assset_style)
            sheet.merge_range(row, 2, row, 4, asset.name, assset_style)

        
            for movement in movements:
                row += 1
                sheet.write(row, 3, movement.location_id.name if movement.location_id else '')
                sheet.write(row, 4, movement.employee_id.name if movement.employee_id else '')
                # sheet.merge_range(row, 0, row, 3, movement.location_id.name)

            row += 1
            c += 1


class AssetReport(models.AbstractModel):
    _name = 'report.stadia.asset_report'
    _inherit = 'report.report_xlsx.abstract'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = []
        return {
            'lines': docids,
            'doc_model': 'stadia.asset',
            'docs': docs
        }

    @api.model
    def _get_report_data(self, date):
        asset_report = []
        if date:
            assets = self.env['stadia.asset'].search([])
            total_days = (date.year % 4) and 365 or 366
            for ast in assets:
                amount = 0
                residual_amount = ast.gross_value
                purchase_and_depreciation_days = abs((ast.purchase_date - date.date()).days)
                if(purchase_and_depreciation_days > 0):
                    rate = (purchase_and_depreciation_days * ast.ifrs_rate)/total_days
                    amount = ast.gross_value * rate
                    residual_amount -= amount
                    current_amount = ast.gross_value * ast.ifrs_rate
                    vals = {
                        'purchase_date': ast.purchase_date,
                        'name': ast.name,
                        'reference_no': ast.reference_no,
                        'partner_id': ast.partner_id,
                        'cpv': ast.cpv,
                        'current_movement_location_id': ast.current_movement_location_id,
                        'current_movement_employee_id': ast.current_movement_employee_id,
                        'id_t_no': ast.id_t_no,
                        'ifrs_rate': ast.ifrs_rate,
                        'gross_value': ast.gross_value,
                        'days': purchase_and_depreciation_days,
                        'amount': amount,
                        'current_amount': current_amount,
                        'remaining_value': residual_amount,
                        'depreciated_value': ast.gross_value - residual_amount,
                        'depreciation_date': ast.purchase_date,
                    }
                    asset_report.append(vals)

        return asset_report

    @api.model
    def get_html(self, date=False):
        datas = []
        if date:
            datas = self._get_report_data(datetime.strptime(date, '%Y-%m-%d'))
        res = {}
        res['lines'] = self.env.ref('stadia.asset_report_template')._render({'data': datas})
        return res

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': True})
        # sheet.set_column(0, 0, 200)
        assets = self._get_report_data(self._parse_date(data['context']['date']))
        # Xlsx Report Header
        sheet.write(0, 0, 'የተገዛበት ቀን', bold)
        sheet.write(0, 1, 'መግለጫ', bold)
        sheet.write(0, 2, 'የደረሰኝ ቁጥር', bold)
        sheet.write(0, 3, 'የአቅራቢ ሥም', bold)
        sheet.write(0, 4, 'የሂሳብ ማወራረሻ', bold)
        sheet.write(0, 5, 'ንብረቱ የሚገኝበት ቦታ', bold)
        sheet.write(0, 6, 'ንብረቱ የሚገኝበት ሰራተኛ', bold)
        sheet.write(0, 7, 'መለያ ቁጥር', bold)
        sheet.write(0, 8, 'IFRS % [rate]', bold)
        sheet.write(0, 9, 'ዋጋ', bold)
        sheet.write(0, 10, 'የእርጅና ቅናሽ', bold)
        sheet.write(0, 11, 'የተጠራቀመ የእርጅና ቅናሽ', bold)
        sheet.write(0, 12, 'የተጣራው የእቃው ዋጋ(ብር)', bold)

        sheet.write(1, 0, 'Date of Purchase', bold)
        sheet.write(1, 1, 'Description', bold)
        sheet.write(1, 2, 'Reference no', bold)
        sheet.write(1, 3, 'Supplier Name', bold)
        sheet.write(1, 4, 'Accounts Ref', bold)
        sheet.write(1, 5, 'Location', bold)
        sheet.write(1, 6, 'Name', bold)
        sheet.write(1, 7, 'ID.T.No.', bold)
        sheet.write(1, 8, 'IFRS % [rate]', bold)
        sheet.write(1, 9, 'Cost', bold)
        sheet.write(1, 10, 'Deperciation Amount', bold)
        sheet.write(1, 11, 'ACC. Depreciation   /IFRS', bold)
        sheet.write(1, 12, 'NBV/IFRS', bold)
        
        row = 2
        for obj in assets:
            sheet.write(row, 0, obj['purchase_date'].strftime('%m/%d/%Y'))
            sheet.write(row, 1, obj['name'])
            sheet.write(row, 2, obj['reference_no'] if obj['reference_no'] else ' ')
            sheet.write(row, 3, obj['partner_id']['name'] if obj['partner_id']['name'] else ' ')
            sheet.write(row, 4, obj['cpv'] if obj['cpv'] else ' ')
            sheet.write(row, 5, obj['current_movement_location_id']['name'] if obj['current_movement_location_id']['name'] else ' ')
            sheet.write(row, 6, obj['current_movement_employee_id']['name'] if obj['current_movement_employee_id']['name'] else ' ')
            sheet.write(row, 7, obj['id_t_no'] if obj['id_t_no'] else ' ')
            sheet.write(row, 8, obj['ifrs_rate'] if obj['ifrs_rate'] else ' ')
            sheet.write(row, 9, obj['gross_value'])
            sheet.write(row, 10, '%.2f' % obj['current_amount'])
            sheet.write(row, 11, '%.2f' % obj['depreciated_value'])
            sheet.write(row, 12, '%.2f' % obj['remaining_value'])
            row +=1

    def _parse_date(self, date=False):
        date_parsed = date
        if date:
            date_parsed = datetime.strptime(date, '%Y-%m-%d')
        return date_parsed

    def get_asset_category(self):
        asset_categories = self.env['stadia.asset.category'].search([])
        return asset_categories


