# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import models, fields, api, exceptions, _


class AttendanceConf(models.Model):
    _name = 'ip.conf'
    _description = 'IP Conf'

    ip = fields.Char(string="IP",required=True)
