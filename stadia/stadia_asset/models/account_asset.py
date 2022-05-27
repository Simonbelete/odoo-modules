from odoo import fields, api, models

class AccountAssetAsset(models.Model):
    _inherit = 'account.asset.asset'

    asset_specification_ids = fields.Many2many('asset.specification')