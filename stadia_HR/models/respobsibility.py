from odoo import fields, models, _, api
import datetime

from odoo.fields import One2many

class Responsibillity(models.Model):
    _name = "hr.responsibility"
    _description = "Employee Responsibility"
    property_id = fields.Many2one('hr.employee', string="Property Name")
    property_name = fields.Char(string="Property Name")
    property_type = fields.Char(string="Property Type")
    tag_number = fields.Char(string="Tag Number")
    money = fields.Char(string="Money")
    amount = fields.Integer(string="Amount")
    employee_supervision = fields.Many2one('hr.employee', string="Employee Supervision")
    number = fields.Integer(string="Number")
    document = fields.Binary(string="Document")
    document_name = fields.Char()
