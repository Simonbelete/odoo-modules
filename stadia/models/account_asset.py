import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from odoo import fields, api, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero

class AccountAssetCategory(models.Model):
    _inherit = 'account.asset.category'

    account_asset_id = fields.Many2one('account.account', string='Asset Account',
                                       required=False,
                                       domain=[('internal_type','=','other'), ('deprecated', '=', False)],
                                       help="Account used to record the purchase of the asset at its original price.")
    account_depreciation_id = fields.Many2one('account.account',
                                              string='Depreciation Entries: Asset Account',
                                              required=False, domain=[('internal_type','=','other'), ('deprecated', '=', False)],
                                              help="Account used in the depreciation entries, to decrease the asset value.")
    account_depreciation_expense_id = fields.Many2one('account.account',
                                                      string='Depreciation Entries: Expense Account',
                                                      required=False,
                                                      domain=[('internal_type','=','other'), ('deprecated', '=', False)],
                                                      help="Account used in the periodical entries,"
                                                           " to record a part of the asset as expense.")
    journal_id = fields.Many2one('account.journal', string='Journal', required=False)

class AccountAssetAsset(models.Model):
    _inherit = 'account.asset.asset'

    cpv = fields.Char()
    asset_movement_ids = fields.One2many('asset.movement', 'asset_id')
    # Holds approved asset movement
    current_movement_id = fields.Many2one('asset.movement')
    current_movement_location_id = fields.Many2one(related="current_movement_id.location_id")
    current_movement_employee_id = fields.Many2one(related="current_movement_id.employee_id")
    asset_movement_count = fields.Integer(compute='_compute_asset_movement_count')

    def _compute_asset_movement_count(self):
        count = 0
        for am in self.asset_movement_ids:
           if(am.state == 'approved'):
               count = count + 1
        self.asset_movement_count = count

    def compute_depreciation_board(self):
        self.ensure_one()

        posted_depreciation_line_ids = self.depreciation_line_ids.filtered(lambda x: x.move_check).sorted(key=lambda l: l.depreciation_date)
        unposted_depreciation_line_ids = self.depreciation_line_ids.filtered(lambda x: not x.move_check)

        # Remove old unposted depreciation lines. We cannot use unlink() with One2many field
        commands = [(2, line_id.id, False) for line_id in unposted_depreciation_line_ids]

        # Calculate depreciation by date 
        # if(self.date < self.first_depreciation_manual_date):
        #     no_of_days_between = (self.first_depreciation_manual_date - self.date).days
        #     days_perecentage = (no_of_days_between * self.method_progress_factor)/365
        #     days_amount = days_perecentage * self.value,
        #     days_vals = {
        #         'amount': days_amount,
        #         'asset_id': self.id,
        #         'sequence': 0,
        #         'name': (self.code or '') + '/' + str(0),
        #         'remaining_value': self.value - days_amount,
        #         'depreciated_value': days_amount,
        #         'depreciation_date': self.date,
        #     }

        if self.value_residual != 0.0:
            amount_to_depr = residual_amount = self.value_residual

            # if we already have some previous validated entries, starting date is last entry + method period
            if posted_depreciation_line_ids and posted_depreciation_line_ids[-1].depreciation_date:
                last_depreciation_date = fields.Date.from_string(posted_depreciation_line_ids[-1].depreciation_date)
                depreciation_date = last_depreciation_date + relativedelta(months=+self.method_period)
            else:
                # depreciation_date computed from the purchase date
                depreciation_date = self.date
                if self.date_first_depreciation == 'last_day_period':
                    # depreciation_date = the last day of the month
                    depreciation_date = depreciation_date + relativedelta(day=31)
                    # ... or fiscalyear depending the number of period
                    if self.method_period == 12:
                        depreciation_date = depreciation_date + relativedelta(month=int(self.company_id.fiscalyear_last_month))
                        depreciation_date = depreciation_date + relativedelta(day=int(self.company_id.fiscalyear_last_day))
                        if depreciation_date < self.date:
                            depreciation_date = depreciation_date + relativedelta(years=1)
                elif self.first_depreciation_manual_date and self.first_depreciation_manual_date != self.date:
                    # depreciation_date set manually from the 'first_depreciation_manual_date' field
                    depreciation_date = self.first_depreciation_manual_date

            total_days = (depreciation_date.year % 4) and 365 or 366
            month_day = depreciation_date.day
            undone_dotation_number = self._compute_board_undone_dotation_nb(depreciation_date, total_days)

            for x in range(len(posted_depreciation_line_ids), undone_dotation_number + 1):
                sequence = x + 1
        
                if(self.date < self.first_depreciation_manual_date and x == 0):
                    amount = 90
                else:
                    amount = self._compute_board_amount(sequence, residual_amount, amount_to_depr,
                                                        undone_dotation_number, posted_depreciation_line_ids,
                                                        total_days, depreciation_date)

                amount = self.currency_id.round(amount)
                print('0000000000000000000000000000000000000')
                print(amount)
                print('0000000000000000000000000000000000000')
                # if float_is_zero(amount, precision_rounding=self.currency_id.rounding):
                #     continue
                residual_amount -= amount
                vals = {
                    'amount': amount,
                    'asset_id': self.id,
                    'sequence': sequence,
                    'name': (self.code or '') + '/' + str(sequence),
                    'remaining_value': residual_amount,
                    'depreciated_value': self.value - (self.salvage_value + residual_amount),
                    'depreciation_date': self.date if x == 0 else depreciation_date,
                    # 'depreciation_date': depreciation_date,
                }

                commands.append((0, False, vals))

                depreciation_date = depreciation_date + relativedelta(months=+self.method_period)

                if month_day > 28 and self.date_first_depreciation == 'manual':
                    max_day_in_month = calendar.monthrange(depreciation_date.year, depreciation_date.month)[1]
                    depreciation_date = depreciation_date.replace(day=min(max_day_in_month, month_day))

                # datetime doesn't take into account that the number of days is not the same for each month
                if not self.prorata and self.method_period % 12 != 0 and self.date_first_depreciation == 'last_day_period':
                    max_day_in_month = calendar.monthrange(depreciation_date.year, depreciation_date.month)[1]
                    depreciation_date = depreciation_date.replace(day=max_day_in_month)

        self.write({'depreciation_line_ids': commands})

        return True