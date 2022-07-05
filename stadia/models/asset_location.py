from odoo import fields, api, models

class AssetLocation(models.Model):
    _name = 'asset.location'
    _sql_constraints = [
        ('name_unique', 'unique (name)', 'Asset location name already exists' )
    ]

    name = fields.Char(required=True)
    is_store = fields.Boolean()