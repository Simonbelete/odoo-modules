from odoo import api, fields, models, _

from attr import exceptions
from odoo.exceptions import ValidationError


class EmployeeResume(models.Model):
    _inherit = 'hr.resume.line'
    name = fields.Char()
    job_title = fields.Char(string="Job Title")
    name_of_organization = fields.Char(string="Name Of Organization")
    salary = fields.Char(string="Salary")
