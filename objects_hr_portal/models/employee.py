# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import models, fields, api, exceptions, _


class hr_portal(models.Model):
    _inherit = 'hr.employee'

    linkedin = fields.Char('LinkedIn')
    employement_type_id = fields.Many2one('hr.contract.type')
    seniority_level = fields.Selection([
        ('junior','Junior'),('mid','Mid'),('senior','Senior'),('team_lead','Team Lead')
      ],string="Seniority Level")    
    work_from_home_days = fields.Integer('Number Of Days',default=10)
    has_permission = fields.Boolean('Has Permission',default=False)
    permission_datetime = fields.Datetime(string='Permission Date Time',default=fields.Datetime.now())
    attendance_type = fields.Selection([('from_home','From Home'),('from_office','From Office')],string="Attendance Type",default="from_home")


    def name_get(self):
        result = []
        for employee in self:
            name = f"{employee.first_name} {employee.last_name}" if (employee.first_name and employee.last_name) else employee.name
            result.append((employee.id, name))
        return result


    def portal_action_attendance_action_change(self):
        """ Check In/Check Out action
            Check In: create a new attendance record
            Check Out: modify check_out field of appropriate attendance record
        """
        self.ensure_one()
        action_date = fields.Datetime.now()
        if self.attendance_state != 'checked_in':
            vals = {
                'employee_id': self.id,
                'check_in': action_date,
            }
            return self.env['hr.attendance'].create(vals)
        attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id), ('check_out', '=', False)],
                                                      limit=1)
        if attendance:
            attendance.check_out = action_date
        else:
            raise exceptions.UserError(
                _('Cannot perform check out on %(empl_name)s, could not find corresponding check in. '
                  'Your attendances have probably been modified manually by human resources.') % {
                    'empl_name': self.sudo().name, })
        return attendance


