from odoo import fields, api, models
from datetime import datetime, timedelta

class AttendanceCategory(models.Model):
    _name = 'stadia.attendance.category'

    name = fields.Char()


class Regularization(models.Model):
    _name = 'stadia.attendance'
    _rec_name = 'employee_id'

    category_id = fields.Many2one('stadia.attendance.category', required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, ondelete='cascade', index=True)
    reason = fields.Text()
    requested_days = fields.Integer(default=0, compute="_compute_requested_days")
    from_date = fields.Date(required=True)
    to_date = fields.Date(required=True)
    state = fields.Selection([('draft', 'Draft'), ('requested', 'Requested'), ('reject', 'Rejected'),
                                     ('approved', 'Approved')
                                     ], default='draft', track_visibility='onchange', string='State',
                                    help='State')
    is_half_day = fields.Boolean()

    @api.onchange('from_date', 'to_date')
    def _compute_requested_days(self):
        self.ensure_one()
        if(self.from_date and self.to_date):
            self.requested_days = (self.to_date - self.from_date).days + 1

    def action_confirm(self):
        self.ensure_one()
        self.sudo().write({'state': 'requested'})

    def action_reject(self):
        self.write({'state': 'reject'})

    def action_approve(self):
        self.write({'state': 'approved'})
        delta = timedelta(days=1)
        start_date = self.from_date
        end_date = self.to_date + timedelta(days=0)
        weekend = set([6]) # Sunday

        if(self.is_half_day):
            while start_date <= end_date:
                current_date = datetime.combine(start_date, datetime.min.time())
                if(current_date.weekday() not in weekend):
                    self.env['hr.attendance'].sudo().create({
                        'check_in': datetime.combine(current_date, datetime.min.time()),
                        'check_out': datetime.combine(current_date, datetime.min.time()) + timedelta(hours=4), # 4 Q: hrs including lunch
                        'regularization': True,
                        'regularization_id': self.id,
                        'employee_id': self.employee_id.id,
                    })
                start_date += delta
        else:
            while start_date <= end_date:
                current_date = datetime.combine(start_date, datetime.min.time())
                if(current_date.weekday() not in weekend):
                    self.env['hr.attendance'].sudo().create({
                        'check_in': datetime.combine(current_date, datetime.min.time()),
                        'check_out': datetime.combine(current_date, datetime.min.time()) + timedelta(hours=9), # 9hrs including lunch
                        'regularization': True,
                        'regularization_id': self.id,
                        'employee_id': self.employee_id.id,
                    })
                start_date += delta
