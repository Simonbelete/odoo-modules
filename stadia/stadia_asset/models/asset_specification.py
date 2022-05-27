from odoo import fields, api, models

class AssetSpecificationName(models.Model):
    _name = 'asset.specification.name'
    _sql_constraints = [
        ('name_unique', 'unique (name)', 'Asset Specification name already exists' )
    ]

    name = fields.Char()

class AssetSpecification(models.Model):
    _name = 'asset.specification.value'
    _sql_constraints = [
        ('name_unique', 'unique (name)', 'Asset Specification value already exists' )
    ]

    name = fields.Char()


class AssetSpecification(models.Model):
    _name = 'asset.specification'
    _sql_constraints = [
        ('name_id_unique', 'unique (name_id)', 'Asset Specification name ref already exists' )
    ]

    asset_id = fields.Many2one('account.asset.asset')
    name_id = fields.Many2one('asset.specification.name', required=True)
    value_id = fields.Many2one('asset.specification.value', required=True)