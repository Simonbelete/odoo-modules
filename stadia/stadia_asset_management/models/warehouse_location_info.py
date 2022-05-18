import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class StockLocation(models.Model):
    _name = "stadia.warehouse.info"
    _description = 'Stadia warehouse Location'
    _rec_name = "warehouse_name"
    warehouse_name = fields.Char(string="Warehouse Name")
    warehouse_location = fields.Char(string="Warehouse Location")
    warehouse_manager = fields.Many2one('hr.employee', string="Warehouse Manager")
