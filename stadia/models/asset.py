import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import fields, api, models

class AccountAssetCategory(models.Model):
    _name = 'stadia.asset.category'

    name = fields.Char()
    ifrs_rate = fields.Float(string="Degressive Factor", digits="Asset IFRS Rate")

class AssetDepreciationLine(models.Model):
    _name = 'stadia.asset.depreciation.line'

    # For development remove on main
    days = fields.Float()
    sequence = fields.Integer(required=True)
    asset_id = fields.Many2one('stadia.asset')
    amount = fields.Monetary(string='Current Depreciation', required=True)
    remaining_value = fields.Monetary(string='Next Period Depreciation', required=True)
    depreciated_value = fields.Monetary(string='Cumulative Depreciation', required=True)
    depreciation_date = fields.Date('Depreciation Date', index=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  readonly=True,
        default=lambda self: self.env.user.company_id.currency_id.id)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 readonly=True,
                                 default=lambda self: self.env.company)

class AccountAssetAsset(models.Model):
    _name = 'stadia.asset'
    _inherit = ['mail.thread']

    name = fields.Char(required=True)
    category_id = fields.Many2one('stadia.asset.category')
    purchase_date = fields.Date(required=True)
    reference_no = fields.Char()
    partner_id = fields.Many2one('res.partner', string='Supplier Name')
    cpv = fields.Char(string='Accounts Ref')
    id_t_no = fields.Char(string="ID.T.No.")
    gross_value = fields.Monetary(string='Gross Value', required=True)
    salvage_value = fields.Monetary(string='Salvage Value')
    ifrs_rate = fields.Float(string="Degressive Factor", required=True, digits="Asset IFRS Rate")
    depreciation_line_ids = fields.One2many('stadia.asset.depreciation.line', 'asset_id')
    asset_movement_ids = fields.One2many('asset.movement', 'asset_id')
    first_depreciation_date = fields.Date(string="Depreciation Date", required=True)
    # Holds approved asset movement
    current_movement_id = fields.Many2one('asset.movement')
    current_movement_location_id = fields.Many2one(related="current_movement_id.location_id")
    current_movement_employee_id = fields.Many2one(related="current_movement_id.employee_id")
    asset_movement_count = fields.Integer(compute='_compute_asset_movement_count')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  readonly=True,
        default=lambda self: self.env.user.company_id.currency_id.id)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 readonly=True,
                                 default=lambda self: self.env.company)

    @api.model
    def create(self, vals):
        asset = super(AccountAssetAsset, self.with_context(mail_create_nolog=True)).create(vals)
        asset.sudo().compute_depreciation_board()
        return asset

    @api.onchange('category_id')
    def _get_category_ifrs_rate(self):
        self.ifrs_rate= self.category_id.ifrs_rate

    def _compute_asset_movement_count(self):
        count = 0
        for am in self.asset_movement_ids:
           if(am.state == 'approved'):
               count = count + 1
        self.asset_movement_count = count

    def compute_depreciation_board(self):
        self.ensure_one()
    
        # total_days = (self.first_depreciation_date.year % 4) and 365 or 366
        total_days = 360
        previous_depreciation_line_ids = self.depreciation_line_ids

        # Remove old depreciation lines
        commands = [(2, line_id.id, False) for line_id in previous_depreciation_line_ids]
        amount = 0
        residual_amount = self.gross_value
        depreciation_date = self.first_depreciation_date
        month_day = depreciation_date.day
        # holds if the purchase date and depreciation date is already calculated
        check_p_and_d_run = False
        i = 0
        # Loop through depreciation until zero or close to zero
        while residual_amount > 0:
            i += 1
            # Get the number of day between purchase date and depreciation date
            purchase_and_depreciation_days = abs((self.purchase_date - self.first_depreciation_date).days)
            if(purchase_and_depreciation_days > 0 and check_p_and_d_run == False):
                rate = (purchase_and_depreciation_days * self.ifrs_rate)/total_days
                amount = self.gross_value * rate
                residual_amount -= amount
                val = {
                    'sequence': i,
                    'days': purchase_and_depreciation_days,
                    'amount': amount,
                    'asset_id': self.id,
                    'remaining_value': residual_amount,
                    'depreciated_value': self.gross_value - residual_amount,
                    'depreciation_date': self.purchase_date,
                }
                commands.append((0, False, val))
                check_p_and_d_run = True
                continue

            amount = self.gross_value * self.ifrs_rate
            residual_amount -= amount
            vals = {
                'sequence': i,
                'days': total_days,
                'amount': amount,
                'asset_id': self.id,
                'remaining_value': residual_amount if(residual_amount > 0) else 0,
                'depreciated_value': self.gross_value - residual_amount,
                'depreciation_date': depreciation_date,
            }
            commands.append((0, False, vals))

            depreciation_date = depreciation_date + relativedelta(months=+12)

            if month_day > 28:
                max_day_in_month = calendar.monthrange(depreciation_date.year, depreciation_date.month)[1]
                depreciation_date = depreciation_date.replace(day=min(max_day_in_month, month_day))


        self.write({'depreciation_line_ids': commands})