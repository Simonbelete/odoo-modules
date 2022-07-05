from multiprocessing.context import assert_spawning
from odoo import fields, api, models
from datetime import datetime


class AssetMovement(models.Model):
    _name = 'asset.movement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'asset_id'

    @api.depends('asset_id')
    def _compute_previous_movement_id(self):
        self.previous_movement_id = self.asset_id.current_movement_id

    ref_no = fields.Char()
    asset_id = fields.Many2one('stadia.asset', required=True)
    previous_movement_id = fields.Many2one('asset.movement', store=True, compute=_compute_previous_movement_id)
    previous_movement_location_id = fields.Many2one(related='previous_movement_id.location_id', store=True)
    previous_movement_employee_id = fields.Many2one(related='previous_movement_id.employee_id', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('declined', 'Declined')
    ], default='draft')
    note = fields.Text()
    date = fields.Date(default=datetime.today())

    location_id = fields.Many2one('asset.location')
    employee_id = fields.Many2one('hr.employee')

    @api.model
    def create(self, vals):
        res = super(AssetMovement, self).create(vals)
        if(vals['state'] == 'approved'):
            res.sudo().action_approve()
        return res

    def action_request(self):
        users = self.env.ref('stadia.group_base_hr').users
        for user in users:
            if(user.active == True):
                self.activity_schedule('stadia.mail_act_asset_movement_approval', user_id=user.id, summary='Asset Movement Approval', note=f'Please Approve {self.asset_id}')
        for record in self:
            record.write({'state': 'requested'})

    def action_approve(self):
        self.write({'state': 'approved', 'previous_movement_id': self.asset_id.current_movement_id})
        id = self.id
        asset_id = self.asset_id.id
        asset = self.env['stadia.asset'].search([('id', '=', asset_id)])
        asset.write({'current_movement_id': id})
        self.schedule_activity_done()

    def action_decline(self):
        """ Decline acquisition request, stop recruiting """
        for record in self:
            record.write({'state': 'declined'})

    def schedule_activity_done(self):
        activity = self.env['mail.activity'].search([
            ('res_id', '=', self.id), 
            ('user_id', '=', self.env.user.id), 
            ('activity_type_id', '=', self.env.ref('stadia.mail_act_asset_movement_approval').id)
            ])
        activity.action_feedback(feedback='Approved')
        other_activity = self.env['mail.activity'].search([
            ('res_id', '=', self.id), 
            ('activity_type_id', '=', self.env.ref('stadia.mail_act_asset_movement_approval').id)
            ])
        other_activity.unlink()