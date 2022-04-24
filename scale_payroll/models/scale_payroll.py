from odoo import models, fields, api

from datetime import datetime
from stdnum.exceptions import ValidationError


class ManufacturingInhirited2(models.Model):
    _inherit = 'hr.contract'
    contract_production_id = fields.Many2one('mrp.production')

    # one step
    @api.onchange('employee_id')
    def Onchange_finalTotal(self):
        print(self.employee_id.user_id.name)
        print(self.manufacture_id.emp_id.name)
        print(self.wage)
        for rec in self:
            xy = self.env['mrp.production'].search([])
            print(len(xy))
            print(self.employee_id.name)
            for x in range(len(xy) + 1):
                print('test')

    manufacture_id = fields.Many2many('mrp.production', delegate=True)

    tip_confirmation = fields.Float(string="Tip Confirmation")

    #
    @api.depends('manufacture_id.calculated_price')
    def _totalTip(self):
        # x = 'NewId_' + str(self.employee_id.id)
        # print(x)
        x = 'NewId_' + str(self.employee_id.id)
        y = str(self.manufacture_id.emp_id)

        if x == y:
            self.tip = self.manufacture_id.calculated_price
        else:
            self.tip = 0

            #
            # print("Product Used", test_data.manufacture_id.product_qty)
            # print("User Id", test_data.employee_id.id)
            # print("User Name", test_data.employee_id.name)
            # print("Worker", test_data.manufacture_id.emp_id.id)

    date_diff = fields.Char(string="Date difference")

    @api.onchange('date_start', 'date_end')
    def _date_difference(self):
        for record in self:
            if self.date_start and self.date_end:
                d1 = datetime.strptime(str(self.date_start), '%Y-%m-%d')
                d2 = datetime.strptime(str(self.date_end), '%Y-%m-%d')
                d3 = d2 - d1
                record.date_diff = str(d3.days)
                print(record.date_diff)
                if record.date_diff == '45':
                    record.hr_responsible_id.notify_success(
                        'Please Update %s Profile The Probation Period is Completed' % (
                            record.employee_id.name))

# class RelateUser(models.Model):
#     _inherit = "res.users"
#
#     related_user_new = fields.Many2one('hr.employee', string="Related Employee")
# for record in self:
#     if record.date_start > record.first_contract_date:
#         raise ValidationError('Start date should not greater than end date.')
#     else:
#         record.date_diff = (record.date_start - record.first_contract_date).days
