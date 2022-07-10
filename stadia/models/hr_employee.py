from odoo import fields, api, models

class EmployeeRelation(models.Model):
    _name = 'hr.employee.relation'

    name = fields.Char(string='Relationship')

class HrEmployeeFamily(models.Model):
    _name = 'hr.employee.family'

    name = fields.Char()
    employee_id = fields.Many2one('hr.employee')
    relation_id = fields.Many2one('hr.employee.relation')

class HrField(models.Model):
    _name = 'hr.field.study'

    name = fields.Char(required=True)

class HrDegree(models.Model):
    _name = 'hr.degree'

    name = fields.Char(required=True)

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
    joining_date = fields.Date(string='Joining Date', help="Employee joining date computed from the contract start date",compute='_compute_joining', store=True)
    education_id = fields.Many2one('hr.field.study', string="Specialized In")
    degree_id = fields.Many2one('hr.degree')
    year_of_experience = fields.Integer()
    year_of_experience_relate_to_job = fields.Integer()
    

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


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    work_place_id = fields.Many2one(related='contract_id.work_place_id', store=True)
    promotion_count = fields.Integer(default=0, compute="_compute_promotion_count")
    asset_count = fields.Integer(default=0, compute="_compute_asset_count")

    def _compute_asset_count(self):
        self.ensure_one()
        asset_count = self.env['stadia.asset'].search_count([('current_movement_employee_id', '=', self.id)])
        self.asset_count = asset_count

    def _compute_promotion_count(self):
        self.ensure_one()
        last_stage_id = self.env['stadia.promotion.stage'].search([])
        last_stage_id = max(last_stage_id.mapped('sequence'))
        promotions_count = self.env['stadia.promotion'].search_count([('employee_id', '=', self.id), ('stage_id', '=', last_stage_id)])
        self.promotion_count = promotions_count


    @api.model
    def create(self, values):
        employee = super(HrEmployee, self).create(values)
        users = self.env.ref('stadia.group_base_system_admin').users
        for user in users:
            if(user.active == True):
                employee.sudo().activity_schedule('stadia.mail_act_employee_creation', user_id=user.id, summary='Give user acess to odoo', note=f'Please Create credentials for {self.name} with the corresponding credentials')
        return employee

    @api.depends('contract_id')
    def _compute_joining(self):
        if self.contract_id:
            date = min(self.contract_id.mapped('date_start'))
            self.joining_date = date
        else:
            self.joining_date = False

    def action_create_user(self):
        """ Check the employee job position and create user base on that"""
        return