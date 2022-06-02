from odoo import fields, api, models

class AssetRequest(models.Model):
    _name = 'asset.asset.request'

    request_by = fields.Many2one('hr.employee')
    # Request to 
    employee_id = fields.Many2one('hr.employee')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ], default='draft', )
    asset_id = fields.Many2one('account.asset.asset')
    note = fields.Text()