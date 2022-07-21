from odoo import api, fields, models

class EsignTemplate(models.Model):
    """ Template to be signed """
    _name = 'esign.template'

    name = fields.Char('Name')
    is_favorite = fields.Boolean(default='Fasle')
    color = fields.Integer('Color Index')
    attachment_id = fields.Many2one('ir.attachment', string='Attachment')
    active = fields.Boolean('Active', default=True)