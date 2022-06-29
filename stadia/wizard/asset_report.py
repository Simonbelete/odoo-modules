from odoo import api, fields, models

class AssetMovementReportWizard(models.TransientModel):
    _name = 'asset.movement.report'

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)

    def print_report(self):
        return True