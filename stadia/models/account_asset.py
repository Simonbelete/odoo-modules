from odoo import fields, api, models

class AccountAssetAsset(models.Model):
    _inherit = 'account.asset.asset'

    asset_movement_ids = fields.One2many('asset.movement', 'asset_id')
    current_movement_id = fields.Many2one('asset.movement')
    asset_movement_count = fields.Integer(compute='_compute_asset_movement_count')

    def _compute_asset_movement_count(self):
        count = 0
        for am in self.asset_movement_ids:
           if(am.state == 'approved'):
               count = count + 1
        self.asset_movement_count = count