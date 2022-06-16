from odoo import fields, api, models

class EmployeeRelation(models.Model):
    _name = 'hr.employee.relation'

    name = fields.Char(string='Relationship')

class HrEmployeeFamily(models.Model):
    _name = 'hr.employee.family'

    employee_id = fields.Many2one('hr.employee')
    relation_id = fields.Many2one('hr.employee.relation')