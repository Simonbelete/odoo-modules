from odoo import fields, api, models

class WorkPlace(models.Model):
    """ Includes Headoffice and projects names """
    _name = 'stadia.workplace'

    name = fields.Char(requried=True)
    place_type = fields.Selection([
        ('head office', 'Head Office'),
        ('project', 'Project')
    ], default='project')