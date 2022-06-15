from odoo import fields, api, models

class HrEmployeeBase(models.AbstractModel):
    _inherit = 'hr.employee.base'

    title = fields.Selection([
        ('ato', 'Ato'),
        ('wt', 'W/t'),
        ('wro', 'W/ro')
    ], required=True)
    promotion_count = fields.Integer(default=0)
    sub_city_id = fields.Many2one('subcity')
    woreda = fields.Char()
    house_number = fields.Char()
    tin_no = fields.Char()
    pension_no = fields.Char()