# -*- coding: utf-8 -*-

from odoo import models, fields, api,SUPERUSER_ID
from odoo import models, fields, api, exceptions, _
from odoo.addons.resource.models.resource import float_to_time, HOURS_PER_DAY
from datetime import datetime, timedelta, time
from pytz import timezone, UTC
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_compare, format_date
from datetime import date, timedelta,datetime
import logging
_logger = logging.getLogger(__name__)

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    def auto_checkout(self):
        attendance_ids = self.env['hr.attendance'].search([('check_in','!=',False),('check_out','=',False)])
        for attendance in attendance_ids:
            # attendance.unlink()
            attendance.write({
                            'check_out': fields.Datetime.from_string(attendance.check_in + timedelta(minutes=1)),
                            'summary': 'Forget to Check out'
                        })
        employees_has_permission = self.env['hr.employee'].search([('has_permission','=',True)])
        for employee in employees_has_permission:
            employee.has_permission = False




        #create WFH for absent employees
        # today = date.today()
        # formatted_date = today.strftime('%Y-%m-%d')
        # if today.day < 26:
        #     # Go back one month
        #     first_day = (today.replace(day=1) - timedelta(days=1)).replace(day=26)
        #     last_day = today.replace(day=25)
        # else:
        #     first_day = today.replace(day=26)
        #     next_month = today.replace(day=28) + timedelta(days=4)
        #     last_day = next_month.replace(day=25)
        # first_day_str = first_day.strftime('%Y-%m-%d')
        # last_day_str = last_day.strftime('%Y-%m-%d')
        # work_from_home_id = self.env.ref('objects_hr_portal.work_from_home_type_id').id
        # tag_id =  self.env['hr.employee.category'].with_user(SUPERUSER_ID).search([('name','=','No-ATTENDANCE')],limit=1)
        # attendance_domain = [('check_in','>=',f"{formatted_date} 00:00"),('check_in','<=',f"{formatted_date} 23:59"),('check_in','!=',False)]
        # today_attendance_ids = self.env['hr.attendance'].with_user(SUPERUSER_ID).search(attendance_domain)
        # today_leave_ids = self.env['hr.leave'].with_user(SUPERUSER_ID).search([('holiday_status_id','!=',work_from_home_id),('request_date_from','<=',formatted_date),('request_date_to','>=',formatted_date),('state','!=','refuse')])
        # today_emp_ids = today_leave_ids.mapped('employee_id.id') + today_attendance_ids.mapped('employee_id.id')
        # absent_employee_ids = self.env['hr.employee'].with_user(SUPERUSER_ID).search([('id','not in',today_emp_ids),('category_ids','!=',tag_id.id)])
        # for absent in absent_employee_ids:            
        #     allocated =(absent.count_employee_leave_allocation_rest_taken_by_date_and_type(self.env.ref('objects_hr_portal.work_from_home_type_id'),datetime.strptime(first_day_str, "%Y-%m-%d").date(),datetime.strptime(last_day_str, "%Y-%m-%d").date()))[0]
        #     taken = (absent.count_employee_leave_allocation_rest_taken_by_date_and_type(self.env.ref('objects_hr_portal.work_from_home_type_id'),datetime.strptime(first_day_str, "%Y-%m-%d").date(),datetime.strptime(last_day_str, "%Y-%m-%d").date()))[1]                  
        #     if allocated - taken > 0:
        #             leave_id = self.env['hr.leave'].with_user(SUPERUSER_ID).create({
        #                 'holiday_type': 'employee',
        #                 'employee_id': absent.id,
        #                 'holiday_status_id': work_from_home_id,
        #                 'employee_ids': [(6,0,[absent.id])],
        #                 'request_date_from': formatted_date,
        #                 'request_date_to': formatted_date,
        #                 'date_from': formatted_date,
        #                 'date_to': formatted_date,
        #                 'name': "Work From Home!!",   
        #                 'number_of_days': 1                                       
        #             })
        #             leave_id.action_approve()
        #             leave_id.action_validate()


class hrLeaveAllocation(models.Model):
    _inherit = 'hr.leave.allocation'


    def create_monthly_allocations(self):

        allocations = []        

        today = datetime.today()
        month = f'0{today.month}' if today.month < 10 else today.month
        month_next = today.month + 1
        month_after = f'0{month_next}' if month_next < 10 else month_next

        employee_ids = self.env['hr.employee'].search([])
        work_from_home_id = self.env.ref("objects_hr_portal.work_from_home_type_id")

        for employee in employee_ids:
              days = 10
              if employee.attendance_type == 'from_home':
                  days = employee.work_from_home_days
              else:
                  today = date.today()
                  # Determine if today is before the 26th — shift to previous month as "custom current month"
                  # if today.day < 26:
                  #     # Go back one month
                  #     first_day = (today.replace(day=1) - timedelta(days=1)).replace(day=26)
                  #     last_day = today.replace(day=25)
                  # else:
                  first_day = today.replace(day=26)
                  # Go to next month
                  next_month = today.replace(day=28) + timedelta(days=4)  # move to next month
                  last_day = next_month.replace(day=25)

                  # Fridays and Saturdays in the full custom month
                  count_fri_sat_per_month = sum(
                      1 for i in range((last_day - first_day).days + 1)
                      if (first_day + timedelta(days=i)).weekday() in (4, 5)
                  )

                  # Total number of days in the custom month
                  total_month_days = (last_day - first_day).days + 1
                  
                  days = (total_month_days - count_fri_sat_per_month) - employee.work_from_home_days

              if days > 0:
                  allocations.append({
                      "name": f'Work From Home {today.replace(month=month_next).strftime("%Y-%m")} ',
                      "holiday_status_id": work_from_home_id.id,
                      "allocation_type": "regular",
                      "holiday_type": "employee",
                      "date_from": f"2025-{month}-26",
                      "date_to": f"2025-{month_after}-25",
                      "number_of_days": days,
                      "employee_id": employee.id,
                      "employee_ids": [(6,0,[employee.id])]
                  })
        
        allocation_ids = self.env['hr.leave.allocation'].create(allocations)
        allocation_ids.action_confirm()
        

class Leave(models.Model):
    _inherit = 'hr.leave'

    pre_leave_request_ids = fields.One2many('pre.leave.request', 'leave_id', string='Pre Leave Requests')
    is_header_visible = fields.Boolean(default=True)



    @api.constrains('date_from', 'date_to', 'employee_id')
    def _check_date(self):
        if self.env.context.get('leave_skip_date_check', False):
            return
        
        work_from_home_id = self.env.ref('objects_hr_portal.work_from_home_type_id')

        all_employees = self.all_employee_ids
        all_leaves = self.search([
            ('date_from', '<', max(self.mapped('date_to'))),
            ('date_to', '>', min(self.mapped('date_from'))),
            ('employee_id', 'in', all_employees.ids),
            ('id', 'not in', self.ids),
            ('state', 'not in', ['cancel', 'refuse']),
            ('holiday_status_id','!=',work_from_home_id.id)
        ])
        for holiday in self:
            domain = [
                ('date_from', '<', holiday.date_to),
                ('date_to', '>', holiday.date_from),
                ('id', '!=', holiday.id),
                ('state', 'not in', ['cancel', 'refuse']),
            ]

            employee_ids = (holiday.employee_id | holiday.employee_ids).ids
            search_domain = domain + [('employee_id', 'in', employee_ids)]
            conflicting_holidays = all_leaves.filtered_domain(search_domain)

            if conflicting_holidays:
                conflicting_holidays_list = []
                # Do not display the name of the employee if the conflicting holidays have an employee_id.user_id equivalent to the user id
                holidays_only_have_uid = bool(holiday.employee_id)
                holiday_states = dict(conflicting_holidays.fields_get(allfields=['state'])['state']['selection'])
                for conflicting_holiday in conflicting_holidays:
                    conflicting_holiday_data = {}
                    conflicting_holiday_data['employee_name'] = conflicting_holiday.employee_id.name
                    conflicting_holiday_data['date_from'] = format_date(self.env, min(conflicting_holiday.mapped('date_from')))
                    conflicting_holiday_data['date_to'] = format_date(self.env, min(conflicting_holiday.mapped('date_to')))
                    conflicting_holiday_data['state'] = holiday_states[conflicting_holiday.state]
                    if conflicting_holiday.employee_id.user_id.id != self.env.uid:
                        holidays_only_have_uid = False
                    if conflicting_holiday_data not in conflicting_holidays_list:
                        conflicting_holidays_list.append(conflicting_holiday_data)
                if not conflicting_holidays_list:
                    return
                conflicting_holidays_strings = []
                if holidays_only_have_uid:
                    for conflicting_holiday_data in conflicting_holidays_list:
                        conflicting_holidays_string = _('From %(date_from)s To %(date_to)s - %(state)s',
                                                        date_from=conflicting_holiday_data['date_from'],
                                                        date_to=conflicting_holiday_data['date_to'],
                                                        state=conflicting_holiday_data['state'])
                        conflicting_holidays_strings.append(conflicting_holidays_string)
                    raise ValidationError(_('You can not set two time off that overlap on the same day.\nExisting time off:\n%s') %
                                          ('\n'.join(conflicting_holidays_strings)))
                for conflicting_holiday_data in conflicting_holidays_list:
                    conflicting_holidays_string = _('%(employee_name)s - From %(date_from)s To %(date_to)s - %(state)s',
                                                    employee_name=conflicting_holiday_data['employee_name'],
                                                    date_from=conflicting_holiday_data['date_from'],
                                                    date_to=conflicting_holiday_data['date_to'],
                                                    state=conflicting_holiday_data['state'])
                    conflicting_holidays_strings.append(conflicting_holidays_string)
                conflicting_employees = set(employee_ids) - set(conflicting_holidays.employee_id.ids)
                # Only one employee has a conflicting holiday
                if len(conflicting_employees) == len(employee_ids) - 1:
                    raise ValidationError(_('You can not set two time off that overlap on the same day for the same employee.\nExisting time off:\n%s') %
                                          ('\n'.join(conflicting_holidays_strings)))
                raise ValidationError(_('You can not set two time off that overlap on the same day for the same employees.\nExisting time off:\n%s') %
                                      ('\n'.join(conflicting_holidays_strings)))



    # @api.model
    # def web_search_read(self, domain=None, fields=None, offset=0, limit=None, order=None, count_limit=None):
        
        
    #     if domain:
    #         work_from_home_id = self.env.ref('objects_hr_portal.work_from_home_type_id').id
    #         domain = ['&', ('holiday_status_id','!=',work_from_home_id)] + domain

    #     # Call the super method with the updated domain and other parameters
    #     return super(Leave, self).web_search_read(
    #         domain=domain,
    #         offset=offset,
    #         limit=limit,
    #         order=order,
    #         count_limit=count_limit,
    #     )

    # @api.model
    # def web_read_group(self, domain=None, fields=None, groupby=None, offset=0, limit=None, orderby=None, lazy=True):

    #     if domain:
    #         work_from_home_id = self.env.ref('objects_hr_portal.work_from_home_type_id').id
    #         domain = ['&', ('holiday_status_id','!=',work_from_home_id)] + domain
                
    #     return super(Leave, self).web_read_group(
    #         domain=domain,
    #         fields=fields,
    #         groupby=groupby,
    #         offset=offset,
    #         limit=limit,
    #         orderby=orderby,
    #         lazy=lazy
    #     )    

    def _get_start_or_end_from_attendance(self, hour, date, employee):
        hour = float_to_time(float(hour))
        holiday_tz = timezone(employee.tz or self.env.user.tz or 'UTC')
        return holiday_tz.localize(datetime.combine(date, hour)).astimezone(UTC).replace(tzinfo=None)

    def action_approve(self):
        res = super().action_approve()
        for rec in self:
          if not all(rec.pre_leave_request_ids.mapped(lambda request: request.state == 'approve')):
              raise ValidationError('requests should be approved first')
        return res