from odoo import fields, api, models


class FieldsOfSpecialization(models.Model):
    _name = 'field.specialization'
    _description = "Specialization"


class EmployeeSpecialization(models.Model):
    _inherit = 'hr.employee'
    fields_of_spec = fields.Many2one('field.specialization', string="Field of Specialization")


class EducationalInformation(models.Model):
    _name = "hr.education"
    _description = "Employee Educational Information"
    name = fields.Text(string="Name")
    employee_id = fields.Many2one('hr.employee')
    type = fields.Selection(
        [('primary', 'Primary Education'), ('secondary', 'Secondary Education'), ('training', 'Training'),
         ('higher', 'Higher Education')])
    certificate = fields.Binary(string="Certificate")
    school_name = fields.Char(string="Name")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    fields_of_study = fields.Char(string="Fields of Study")
    grade = fields.Char(string="Grade", attrs="{'invisible': [('type', 'not in', ['primary', 'secondary'])]}")
