import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class AssetType(models.Model):
    _name = "stadia.asset"
    _description = 'Stadia Asset'
    _rec_name = "name"
    name = fields.Char(string="Asset name")
    description = fields.Text(string="Description")
    responsible_person = fields.Many2one('hr.employee', string="Responsible Person")
    warehouse_location = fields.Many2one('stadia.warehouse.info', string="Warehouse Location")
    tag_number = fields.Char(string="Asset Tag Number")
    asset_category = fields.Many2one('asset.type', string="Asset Category", required=True)
    asset_reference = fields.Char(string="Serial Number")
    created_date = fields.Date(string="Purchased Date")
    gross_value = fields.Float(string="Gross Value")
    salvage_value = fields.Float(string="Salvage Value")
    residual_value = fields.Float(string="Residual Value")
    vendor = fields.Many2one("res.partner", string="Vendor")
    Depreciation_method = fields.Selection(string="Computation Method", related='asset_category.Depreciation_method',
                                           tracking=True)
    Degressive_Factor = fields.Float(string="Degressive Factor", related='asset_category.Degressive_Factor',
                                     tracking=True)
    depreciation_number = fields.Integer(string="Depreciation Number", related="asset_category.depreciation_number",
                                         tracking=True)
    month_number = fields.Integer(string="One Entry Every", related="asset_category.month_number", tracking=True)

    @api.depends("residual_value", "Degressive_Factor", "depreciation_number", "month_number")
    def _calculate_depreciation(self):
        pass
