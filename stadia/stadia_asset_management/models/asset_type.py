import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class AssetType(models.Model):
    _name = "asset.type"
    _description = 'Asset category'
    _rec_name = 'category_name'
    category_name = fields.Char(string="Asset Category Name")
    Depreciation_method = fields.Selection([('linear', 'Linear'), ('degressive', 'Degressive')])
    Degressive_Factor = fields.Float(string="Degressive Factor")
    depreciation_number = fields.Integer(string="Depreciation Number/Life")
    month_number = fields.Integer(string="One Entry Every/Month")
