# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import models, fields, api, exceptions, _


class Penality(models.Model):
    _name = 'hr.penality'
    _description = 'HR Penality'

    employee_id = fields.Many2one('hr.employee',string="Employee")
    date = fields.Date(string='Day',required=True,index=True)
    check_in_date = fields.Datetime(string='Check In Date',required=True,index=True)
    penality_hours = fields.Float(string="Penality Hours")

