from multiprocessing.context import assert_spawning
from odoo import fields, api, models
from datetime import datetime


class AssetMovement(models.Model):
    _name = 'asset.movement'

    @api.depends('asset_id')
    def _compute_previous_movement_id(self):
        self.previous_movement_id = self.asset_id.current_movement_id

    asset_id = fields.Many2one('stadia.asset', required=True)
    previous_movement_id = fields.Many2one('asset.movement', store=True, compute=_compute_previous_movement_id)
    previous_movement_location_id = fields.Many2one(related='previous_movement_id.location_id')
    previous_movement_employee_id = fields.Many2one(related='previous_movement_id.employee_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved')
    ], default='draft')
    note = fields.Text()
    date = fields.Date(default=datetime.today())

    location_id = fields.Many2one('asset.location')
    employee_id = fields.Many2one('hr.employee')

    def action_approve(self):
        self.write({'state': 'approved', 'previous_movement_id': self.asset_id.current_movement_id})
        id = self.id
        asset_id = self.asset_id.id
        asset = self.env['account.asset.asset'].search([('id', '=', asset_id)])
        asset.write({'current_movement_id': id})