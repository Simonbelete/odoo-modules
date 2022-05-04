from odoo import fields, models, _, api
import datetime

from odoo.fields import One2many


class EmployeeDetail(models.Model):
    _inherit = 'hr.employee'
    Hiring_day = fields.Date(placeholder="The name of the University")
    Hire_letter_number = fields.Char(placeholder="The Hire_letter_number")
    _order = 'id asc'
    Entrance_Type = fields.Selection(
        [('permanent', 'Permanent'),
         ('Contract', 'Contract'),
         ('Other', 'Other'),
         ('per-time', 'Per-time')],
        default='Other')

    # def _manufacturing_count(self):
    #     for rec in self:
    #         manufacturing_count = self.env['mrp.production'].search_count([])
    #         rec.manufacturing_count = manufacturing_count
    #
    # def ActionManufacturing_count(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Manufacturing',
    #         'res.model': 'mrp.production',
    #         'domain': [('employee_id', '=', self.id)],
    #         'view_mode': 'tree, form',
    #         'target': 'current',
    #     }

    education_level = fields.Selection(
        [('certificate', 'Certificate'),
         ('diplomat', 'Diplomat'),
         ('degree', 'Degree'),
         ('master', 'Master'),
         ('phd', 'PHD'),
         ('professor', 'Professor'),
         ],
        'education_level', default="degree")
    field_of_study = fields.Char(string='Field of study')
    total_year_of_ex = fields.Char(string="Total Year of Experience")
    # SPOUSE INFORMATION
    phone_spouse = fields.Char(string='Phone Number')

    training_name_ids = fields.One2many('hr.education.list', 'training_name_inverse_id',
                                        '  ')
    employee_emergency_ids = fields.One2many('hr.employee_contact', 'em_full_name_id', '  ')

    employe_education_ids = fields.One2many('hr.education.list', 'employee_name_education_id',
                                            'Higher Educational Information')
    hs_info_ids = fields.One2many('hr.education.list', 'hs_info_id', 'High School Information')
    ps_info_ids = fields.One2many('hr.education.list', 'ps_info_id', 'Primary School Information')
    # SIBLING INFORMATION
    employee_sibling_info_ids = fields.One2many('hr.family.info', 'sibling_info_id',
                                                ' ')
    # CHILD INFORMATION
    child_info_ids = fields.One2many('hr.family.info', 'child_info_id', '  ')

    #     SPOUSE SIBLING INFORMATION
    spouse_sibling_info_ids = fields.One2many('hr.family.info', 'spouse_sibling_id',
                                              '  ')
    contract_employee_id = fields.One2many('hr.contract', 'employee_id')
    responsibility_ids = fields.One2many('hr.responsibility', 'property_id')

    city_id = One2many('hr.employee', 'city_info')

    birthday1 = fields.Date(string="Date of Birth")
    age_com = fields.Char(string="Age", compute="_calculate_age")

    # @api.model
    # def create(self, vals):
    #     vals['work_phone'] = "test"
    #     return super(EmployeeDetail, self).create(vals)

    asset_assignment = fields.Many2one('account.asset.asset')

    # PHONE NUMBER PRiFIX
    def write(self, vals):
        if 'work_phone' in vals:
            if vals['work_phone'].startswith("0"):
                vals['work_phone'] = '+251' + vals['work_phone'][1:]
            else:
                vals['work_phone'] = '+251' + vals['work_phone']

        # override create method for work mobile
        if 'mobile_phone' in vals:
            if vals['mobile_phone'].startswith("0"):
                vals['mobile_phone'] = '+251' + vals['mobile_phone'][1:]
            else:
                vals['mobile_phone'] = '+251' + vals['mobile_phone']
        # overriding create method for house phone number

        if 'tell' in vals:
            if vals['tell'].startswith("0"):
                vals['tell'] = '+251' + vals['tell'][1:]
            else:
                vals['tell'] = '+251' + vals['tell']
        # overriding create method for private mobile number
        if 'mobile_phone_two' in vals:
            if vals['mobile_phone_two'].startswith("0"):
                vals['mobile_phone_two'] = '+251' + vals['mobile_phone_two'][1:]
            else:
                vals['mobile_phone_two'] = '+251' + vals['mobile_phone_two']

        # overriding create method for mother phone number
        if 'm_phone' in vals:
            if vals['m_phone'].startswith("0"):
                vals['m_phone'] = '+251' + vals['m_phone'][1:]
            else:
                vals['m_phone'] = '+251' + vals['m_phone']

        return super(EmployeeDetail, self).write(vals)

    # COMPUTE AGE VALUE BASED ON DATE OF BIRTH
    @api.depends('birthday1')
    def _calculate_age(self):
        today = datetime.date.today()
        for data in self:
            if data.birthday1:
                birthday1 = fields.Datetime.to_datetime(data.birthday1).date()
                total_age = str(int((today - birthday1).days / 365))
                data.age_com = total_age
            else:
                data.age_com = " "

    def copy(self, default={}):
        default['field_of_study'] = "Copy(" + self.field_of_study + ")"
        rtn = super(EmployeeDetail, self).copy(default=default)
        return rtn


# EDUCATIONAL FIlEDS
class EducationalField(models.Model):
    _name = 'hr.education.list'
    employee_name_education_id = fields.Many2one('hr.employee')
    Employe_full_name = fields.Char()
    institute = fields.Char()
    institute_id = fields.Many2one('res.partner', string="Institute")
    CGPA = fields.Float(string='CGPA')
    start_Date = fields.Date(string='Entrance Date')
    end_date = fields.Date(string='Exit Date')
    document_higher_education = fields.Binary()
    program = fields.Selection(
        [('regular', 'Regular'),
         ('distance', 'Distance'),
         ('nights', 'Night')],
        'program', default="regular")

    # high school information
    hs_info_id = fields.Many2one('hr.employee')
    name_school_id = fields.Many2one('res.partner', string='Name of School')
    year = fields.Char(string='Year')
    grade = fields.Char(string='Grade')
    document_high_school = fields.Binary()

    # PRIMARY SCHOOL INFORMATION
    ps_info_id = fields.Many2one('hr.employee')
    name_school_p_id = fields.Many2one('res.partner', string='Name of School')
    year_p = fields.Char(string='Year')
    grade_p = fields.Char(string='Grade')
    document_primary_school = fields.Binary()

    # TRANING INFORMATION
    training_name_inverse_id = fields.Many2one('hr.employee')
    type_of_training = fields.Char(string='Type of Training')
    name_of_institution_id = fields.Many2one('res.partner', string='Name of Institution')
    reward = fields.Char(string='Award')
    document_for_training = fields.Binary()


# EMPLOYEE EXPERIENCE TABLE
class EmployeeResumeDetail(models.Model):
    _inherit = 'hr.resume.line'
    # EXTERNAL
    name_of_org_id = fields.Many2one('res.partner', string='Organization')
    job_title_ex = fields.Char(string='Job Title')
    department_ex = fields.Many2one('hr.department', string='Department')
    ex_n = fields.Integer(string='Number')
    date_start = fields.Date(string="Start Date", required=False)
    from_ex = fields.Date(string="Start Date")
    to_ex = fields.Date(string="End Date")
    document_external_exp = fields.Binary()
    #     INTERNAL
    job_title_in = fields.Char(string="Job Title")
    department_in = fields.Many2one('hr.department', string='Department')
    from_in = fields.Date(string="Start Date")
    to_in = fields.Date(string="End Date")
    in_n = fields.Integer(string="Number")
    document_internal_exp = fields.Binary()


class PrivateInformation(models.Model):
    _inherit = 'hr.employee'
    city_info = fields.Many2one('res.country.state')
    pension_number = fields.Char(string="Pension Number")
    tin_number = fields.Char(string="Tin Number")
    city = fields.Many2one("res.country.state", string="City")
    sub_city = fields.Many2one("res.country.state", string="Sub City")
    woreda = fields.Char(string="Woreda/Kebele")
    house_number = fields.Char(string="House Number")
    mobile_phone_two = fields.Char(string="Mobile Phone")
    tell = fields.Char(string="House Phone Number")
    pr_email = fields.Char(string="Email Address")


# family information
class FamilyInformation(models.Model):
    _inherit = 'hr.employee'
    relative = fields.Char(string="Father Name")
    relativ_two = fields.Char(string="Mother Name")
    m_phone = fields.Char(string="Phone Number")
    full_name = fields.Char(string="Full Name")
    work = fields.Text(string="Work")
    current_address_f = fields.Text(string="Current Address")
    spouse_mother_full_name = fields.Char(string="Mother Name")
    spouse_father_full_name = fields.Char(string="Father Name")
    spouse_date_of_birth = fields.Date(string="Date of Birth")
    spouse_full_name = fields.Char(string="Spouse Full Name")
    spouse_mother_phone = fields.Char(string="Mother Phone")


# Emergency Contact Information
class EmergencyContact(models.Model):
    _name = 'hr.employee_contact'
    em_full_name_id = fields.Many2one('hr.employee')
    em_full_name_id_relation = fields.Many2one('res.partner', string="Full Name")
    em_city = fields.Many2one("res.country.state", string="City")
    em_sub_city = fields.Many2one("res.country.state", string="Sub City")
    em_woreda = fields.Char(string="Woreda/Kebele")
    em_phone = fields.Char(string="Mobile Number")
    em_house = fields.Char(string="House Number")


class PayrollContactDetail(models.Model):
    _inherit = 'hr.contract'
    hra = fields.Char()
    transport = fields.Integer(string='Transport Allowance')
    incentive = fields.Integer(string='Incentive Allowance')
    house = fields.Integer(string='House')
    phone_payroll = fields.Integer(string='Phone Package')
    fuel = fields.Integer(string='Fuel Package')
    total_allowance = fields.Float(compute='_total_allowance', string='Total Allowance')
    forensic_certificate = fields.Binary(string="Forensic Certificate")
    forensic_docname = fields.Char()
    medical_certificate = fields.Binary(string="Medical Certificate")
    medical_docname = fields.Char()
    warranty_certificate = fields.Binary(string="Warranty Certificate")
    warranty_docname = fields.Char()

    # TOTAL ALLOWANCE
    @api.depends('transport', 'incentive', 'house', 'phone_payroll', 'fuel')
    def _total_allowance(self):
        for total_data in self:
            total_data.total_allowance = total_data.transport + total_data.incentive \
                                         + total_data.house + total_data.phone_payroll \
                                         + total_data.fuel


class DeductionContactDetail(models.Model):
    _inherit = 'hr.contract'
    cost_sharing_status = fields.Selection(
        [('yes', 'Yes'),
         ('no', 'No')],
        defualt='no')
    pay_amount = fields.Float(string="How Much")
    tax = fields.Float(compute="_tax", string='Tax')
    pension_d = fields.Integer(string='Pension')
    medical_insurance = fields.Integer(string='Medical Insurance')
    salary_scale = fields.Char(string='Salary Scale')
    loan = fields.Float(string="Employee Loan")
    pension_deduction = fields.Float(compute="_pension", string="Pension")

    # PENSION CALCULATION BASED ON COUNTRY STANDARD
    @api.depends('wage')
    def _pension(self):
        for pension in self:
            pension.pension_deduction = pension.wage * 0.07

    # TAX CALCULATION BASED ON COUNTRY STANDARD
    @api.depends('wage')
    def _tax(self):
        for total_wage in self:
            if total_wage.wage >= 0 and total_wage.wage <= 600:
                total_wage.tax = 0
            elif total_wage.wage > 600 and total_wage.wage <= 1650:
                total_wage.tax = total_wage.wage * 0.1
            elif total_wage.wage > 1650 and total_wage.wage <= 3200:
                total_wage.tax = total_wage.wage * 0.15
            elif total_wage.wage > 3200 and total_wage.wage <= 5250:
                total_wage.tax = total_wage.wage * 0.2
            elif total_wage.wage > 5250 and total_wage.wage <= 7800:
                total_wage.tax = total_wage.wage * 0.25
            elif total_wage.wage > 7800 and total_wage.wage <= 10900:
                total_wage.tax = total_wage.wage * 0.3
            elif total_wage.wage > 10900:
                total_wage.tax = total_wage.wage * 0.35


class FamilyInformation(models.Model):
    # EMPLOYEE SIBLING INFORMATION
    _name = 'hr.family.info'
    sibling_info_id = fields.Many2one('hr.employee')
    em_sibling_full_name = fields.Char(string='Full Name')
    sibling_gender = fields.Selection(
        [('male', 'Male'),
         ('female', 'Female'),
         ('other', 'Other')])
    sibling_current = fields.Char(string='Current Address')
    sibling_phone = fields.Char(string='Phone Number')

    # EMPLOYEE CHILD INFORMATION
    child_info_id = fields.Many2one('hr.employee')
    child_full_name = fields.Char(string='Full Name')
    child_gender = fields.Selection(
        [('male', 'Male'),
         ('female', 'Female'),
         ('other', 'Other')])
    child_current = fields.Char(string='Current Address')
    child_phone = fields.Char(string='Phone Number')
    document_for_brith_certificate = fields.Binary()
    # auto-increament
    #     number_one = fields.Char(string='Number', required=True, copy=False, readonly=True,
    #                              index=True, default=lambda self: _('New'))
    # SPOUSE SIBLING INFORMATION
    spouse_sibling_id = fields.Many2one('hr.employee')
    spouse_sibling_full_name = fields.Char(string='Full Name')
    spouse_sibling_gender = fields.Selection(
        [('male', 'Male'),
         ('female', 'Female'),
         ('other', 'Other')])
    spouse_sibling_current = fields.Char(string='Current Address')
    spouse_sibling_phone = fields.Char(string='Phone Number')


class BranchName(models.Model):
    _name = 'hr.branch'
    _description = 'branch description'
    branch_name = fields.Many2one('res.partner', string="Branch Name")
