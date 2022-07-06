from odoo import fields, api, models

class EducationalInformation(models.Model):
    _name = "hr.education"
    _description = "Employee Educational Information"
    name = fields.Text(string="Name", compute="_compute_name")
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

    def _compute_name(self):
        for record in self:
            if(record.fields_of_study):
                record.name = record.fields_of_study