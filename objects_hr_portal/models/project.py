# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import models, fields, api, exceptions, _


class Project(models.Model):
    _inherit = 'project.project'

    facilitator_id = fields.Many2one('hr.employee',string="Facilitator")
    