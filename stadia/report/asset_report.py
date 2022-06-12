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
    def get_html(self):
        res = {}
        res['lines'] = self.env.ref('stadia.asset_report')._render({'data': {'a': 'b'}})
        return res
