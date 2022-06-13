from datetime import datetime
from odoo import api, models

class AssetReport(models.AbstractModel):
    _name = 'report.stadia.asset_report'

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
                purchase_and_depreciation_days = abs((ast.purchase_date - ast.first_depreciation_date).days)
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
                        'name': ast.name,
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
        res['lines'] = self.env.ref('stadia.asset_report')._render({'data': datas})
        return res
