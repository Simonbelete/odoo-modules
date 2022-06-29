from odoo import api, fields, models

class AssetMovementReportWizard(models.TransientModel):
    _name = 'asset.movement.report'

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)

    def print_report(self):
        self.ensure_one()
        [data] = self.read()
        datas = {
            'ids': [],
            'model': 'stadia.asset',
            'form': data
        }
        return self.env.ref('stadia.asset_movmenet_report').report_action([], data=datas)