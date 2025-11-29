# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import models, fields, api, exceptions, _


class AttendanceConf(models.Model):
    _name = 'attendance.conf'
    _description = 'Attendance Conf'

    check_in_hour = fields.Integer(string="Check In Hour")
    maximum_check_in_hour = fields.Integer(string="Maximum Check In Hour")



class Attendance(models.Model):
    _inherit = 'hr.attendance'

    ip = fields.Char('IP',index=True)
    ip_out = fields.Char('IP Out',index=True)

    check_in_location = fields.Char('Check In Location')
    check_out_location = fields.Char('Check Out Location')

    