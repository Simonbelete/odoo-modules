from odoo import api, fields, models, _

from attr import exceptions
from odoo.exceptions import ValidationError


class EmployeeProfile(models.Model):
    _inherit = "hr.employee"
    family_ids = fields.One2many('hr.family', 'employee_id')
    education_ids = fields.One2many('hr.education', 'employee_id')
    emergency_ids = fields.One2many("hr.emergency.information", "employee_id")
    pension_id = fields.Char(string="Pension Id")
    tin_number = fields.Char(string="Tin Number")

    #     contact information
    city = fields.Char(string="City")
    sub_city = fields.Char(string="Sub City")
    woreda = fields.Char(string="Woreda")
    house_number = fields.Char(string="House Number")
    mobile_number = fields.Char(string="Mobile Number")

    def write(self, vals, context={}):
        if 'mobile_phone' in vals:
            if vals['mobile_phone'].startswith("0"):
                vals['mobile_phone'] = '+251' + vals['mobile_phone'][1:]
            else:
                vals['mobile_phone'] = '+251' + vals['mobile_phone']

        if 'work_phone' in vals:
            if vals['work_phone'].startswith("0"):
                vals['work_phone'] = '+251' + vals['work_phone'][1:]
            else:
                vals['work_phone'] = '+251' + vals['work_phone']

        return super(EmployeeProfile, self).write(vals)


# EMERGENCY CONTACT INFORMATION

class EmergencyInformation(models.Model):
    _name = "hr.emergency.information"
    _description = "Employee Emergency Information"
    employee_id = fields.Many2one('hr.employee')
    name = fields.Char(string="Name")
    city = fields.Char(string="City")
    sub_city = fields.Char(string="Sub City")
    woreda = fields.Char(string="Woreda")
    mobile_number = fields.Char(string="Mobile Number")


class EmployeeFamily(models.Model):
    _name = "hr.family"
    _description = "Employee Family"
    employee_id = fields.Many2one('hr.employee')
    name = fields.Text(string="Name")
    relation_type = fields.Selection(
        [('mother', 'Mother'), ('sister', 'Sister'), ('brother', 'Brother'), ('spouse', 'Spouse'),
         ('spouse_mother', 'Spouse Mother'), ('spouse_sister', 'Spouse Sister'), ('spouse_brother', 'Spouse Brother')])
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender", default="")
    birth_date = fields.Date(string="Birth Day")
    mobile_number = fields.Char(string="Mobile Number")


class EducationalInformation(models.Model):
    _name = "hr.education"
    _description = "Employee Educational Information"
    name = fields.Text(string="Name")
    employee_id = fields.Many2one('hr.employee')
    type = fields.Selection(
        [('primary', 'Primary Education'), ('secondary', 'Secondary Education'), ('training', 'Training'),
         ('higher', 'Higher Education')])
    certificate = fields.Binary(string="Certificate")
    school_name = fields.Char(string="School Name")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    fields_of_study = fields.Char(string="Fields of Study")
    grade = fields.Char(string="Grade", attrs="{'invisible': [('type', 'not in', ['primary', 'secondary'])]}")

# class ActivityRestriction(models.Model):
#     _inherit = "mail.activity"
#
#     def action_done(self):
#         if
#         """ Wrapper without feedback because web button add context as
#         parameter, therefore setting context to feedback """
#         messages, next_activities = self._action_done()
#         return messages.ids and messages.ids[0] or False
