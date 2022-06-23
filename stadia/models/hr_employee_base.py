from odoo import fields, api, models

class HrEmployeeBase(models.AbstractModel):
    _inherit = 'hr.employee.base'

    def _defaultBadgeIdNo(self):
        return '0000/000/00/000/00'

    title = fields.Selection([
        ('ato', 'Ato'),
        ('wt', 'W/t'),
        ('wro', 'W/ro')
    ])
    # city_id = fields.Many2one('stadia.city')
    badge_id_no = fields.Char(string="ID No", copy=False, default=_defaultBadgeIdNo)
    promotion_count = fields.Integer(default=0)
    sub_city_id = fields.Many2one('subcity')
    woreda = fields.Char()
    house_number = fields.Char()
    tin_no = fields.Char()
    pension_no = fields.Char()
    family_ids = fields.One2many('hr.employee.family', 'employee_id')
    emergency_contact_name = fields.Char()
    emergency_contact_city_id = fields.Many2one('subcity')
    emergency_contact_woreda = fields.Char()
    emergency_contact_house_no = fields.Char()
    emergency_contact_relation_id = fields.Many2one('hr.employee.relation')
    education_ids = fields.One2many('hr.education', 'employee_id')
    joining_date = fields.Date(string='Joining Date', help="Employee joining date computed from the contract start date",compute='_compute_joining', store=True)

    def action_generate_badge_id(self):
        next_code = self.env['ir.sequence'].next_by_code('badge.no.sequence')
        id_no = 'STAD/SID/HO/%s' % next_code
        previous_id_no = self.badge_id_no
        self.write({'badge_id_no': id_no})
        # Write to log not incase on accidentally clicked
        self._log_badge_id(previous_id_no, id_no)
        
    def _log_badge_id(self, p_id, n_id):
        message = 'Badge id changed from %s to %s' %(p_id, n_id)
        self.message_post(body=message)