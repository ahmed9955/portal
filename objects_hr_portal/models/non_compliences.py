# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import models, fields, api, exceptions, _

class NoneComplienceCategory(models.Model):
    _name = 'none.compliences.category'
    _description = 'None Compliences Category'

    name = fields.Char('Name')

class NoneComplienceStatus(models.Model):
    _name = 'none.compliences.status'
    _description = 'None Compliences Status'

    name = fields.Char('Name')


class NoneComplience(models.Model):
    _name = 'none.compliences'
    _description = 'None Compliences'

    employee_id = fields.Many2one('hr.employee',string="Assignee")
    description = fields.Char('Description')
    title = fields.Char('Title')



