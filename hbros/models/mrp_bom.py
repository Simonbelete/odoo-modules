from odoo import fields, api, models

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    salary = fields.Float(required=True)