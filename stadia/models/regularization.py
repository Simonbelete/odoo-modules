from odoo import fields, api, models
from datetime import datetime, timedelta

class AttendanceCategory(models.Model):
    _name = 'stadia.attendance.category'

    name = fields.Char()


class Regularization(models.Model):
    _name = 'stadia.attendance'

    category_id = fields.Many2one('stadia.attendance.category', required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, ondelete='cascade', index=True)
    reason = fields.Text()
    from_date = fields.Date(required=True)
    to_date = fields.Date(required=True)
    state = fields.Selection([('draft', 'Draft'), ('requested', 'Requested'), ('reject', 'Rejected'),
                                     ('approved', 'Approved')
                                     ], default='draft', track_visibility='onchange', string='State',
                                    help='State')

    def action_confirm(self):
        self.ensure_one()
        self.sudo().write({'state': 'requested'})

    def action_reject(self):
        self.write({'state': 'reject'})

    def action_approve(self):
        self.write({'state': 'approved'})
        delta = timedelta(days=1)
        start_date = self.from_date
        weekend = set([6]) # Sunday
        while start_date <= self.to_date:
            current_date = datetime.combine(start_date, datetime.min.time())
            if(current_date.weekday() not in weekend):
                self.env['hr.attendance'].sudo().create({
                    'check_in': datetime.combine(current_date, datetime.min.time()),
                    'check_out': datetime.combine(current_date, datetime.min.time()) + timedelta(hours=8),
                    'regularization': True,
                    'employee_id': self.employee_id.id,
                })
            start_date += delta
