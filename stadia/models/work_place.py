from odoo import fields, api, models

class WorkPlace(models.Model):
    """ Includes Headoffice and projects names """
    _name = 'stadia.workplace'

    name = fields.Char(requried=True)
    place_type = fields.Selection([
        ('head office', 'Head Office'),
        ('project', 'Project')
    ], default='project')
    is_favorite = fields.Boolean(default=False)
    employee_count = fields.Integer(default=0, compute="_compute_employee_count")

    def _compute_employee_count(self):
        self.ensure_one()
        count = self.env['hr.employee'].search_count([('contract_id.work_place_id', '=', self.id)])
        self.employee_count = count

    def action_open(self):
        return {
            'name': 'Work Location',
            'type': 'ir.actions.act_window',
            'res_model': 'stadia.workplace',
            'res_id': self.id,
            'view_mode': 'form',
        }