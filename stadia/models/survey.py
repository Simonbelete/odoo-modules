from odoo import fields, api, models

class Survey(models.Model):
    _name = 'stadia.survey'
    _rec_name = 'title'

    title = fields.Char(required=True)
    description = fields.Hmtl(sanitize=False,
        help="This message will be displayed on the top of appraisal")
    active = fields.Boolean(default=True)