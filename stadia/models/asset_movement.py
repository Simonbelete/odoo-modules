from multiprocessing.context import assert_spawning
from odoo import fields, api, models


class AssetMovement(models.Model):
    _name = 'asset.movement'

    asset_id = fields.Many2one('account.asset.asset', required=True)
    previous_movement_location_id = fields.Many2one(related='asset_id.current_movement_id.location_id')
    previous_movement_employee_id = fields.Many2one(related='asset_id.current_movement_id.employee_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved')
    ], default='draft')
    note = fields.Text()
    date = fields.Date()

    location_id = fields.Many2one('asset.location', required=True)
    employee_id = fields.Many2one('hr.employee')

    def action_approve(self):
        asset = self.env['account.asset.asset'].search([('id', '=', self.asset_id.id)])
        asset.write({'current_movement_id': self.id})
        # for record in self:
        #     record.write({'state', 'approved'})