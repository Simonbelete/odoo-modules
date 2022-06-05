from odoo import fields, api, models



class AssetMovement(models.Model):
    _name = 'asset.movement'

    previous_movement_id = fields.Many2one('asset.movement')
    asset_id = fields.Many2one('account.asset.asset', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved')
    ])
    note = fields.Text()
    date = fields.Date()
    # Reference to the assets previous movement
    # current_movement_id = fields.Many2one(related='asset_id.')

    location_id = fields.Many2one('asset.location', required=True)
    employee_id = fields.Many2one('hr.employee')