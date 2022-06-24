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
    employee_count = fields.Integer(default=0)

    def action_open_edit(self):
        form_view = self.env.ref('action_work_place_form')
        print('hhhhhhhhhhhhhhhhh')
        # return {
        #     'name': 'Work Location',
        #     'res_model': 'stadia.workplace',
        #     'res_id': self.id,
        #     'view_mode': 'form'
        # }

    def action_open(self):
        return {
            'name': 'Work Location',
            'type': 'ir.actions.act_window',
            'res_model': 'stadia.workplace',
            'res_id': self.id,
            'view_mode': 'form',
        }