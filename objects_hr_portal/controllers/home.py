from odoo import http,fields,SUPERUSER_ID
from odoo.http import request
from datetime import datetime,date,timedelta,time
import subprocess,re
import socket,requests
import pytz
import base64
import os

class Home(http.Controller):


    @http.route(['/objects/hr/home'], type='http', auth='user', website=True)
    def home(self, **kwargs):


        data = {}
        absent_employees = []
        attendance = []        
        absents = []
        today = date.today()
        formatted_date = today.strftime('%Y-%m-%d')
        current_employees = {}

        time_zone = pytz.timezone(request.env.user.tz or 'UTC')
        current_dt = datetime.now(time_zone)
        current_time = current_dt.time()
        attendance_config = request.env['attendance.conf'].with_user(SUPERUSER_ID).search([],limit=1)
        ten_am = time(attendance_config.check_in_hour, 0)

        current_td = timedelta(hours=current_time.hour, minutes=current_time.minute, seconds=current_time.second)
        ten_am_td = timedelta(hours=ten_am.hour, minutes=ten_am.minute, seconds=ten_am.second)

        # Subtract and get difference in hours
        diff_td = current_td - ten_am_td
        time_diff = diff_td.total_seconds() / 3600

        if time_diff > 0:
            data['start_check_in'] = 'start'
        else:
            data['start_check_in'] = 'end'


        attendance_domain = [('check_in','>=',f"{formatted_date} 00:00"),('check_in','<=',f"{formatted_date} 23:59"),('check_in','!=',False)]

        
        data['type_filter'] = 'both'
        data['both_color'] = 'bg-blue-100 text-blue-700'
        data['home_color'] = 'bg-gray-100'
        data['office_color'] = 'bg-gray-100'

        if 'type_filter' in kwargs:
            data['type_filter'] = kwargs['type_filter']
            if kwargs['type_filter'] != 'both':
                attendance_domain.append(('attendance_location','=',kwargs['type_filter']))

                if kwargs['type_filter'] == 'home':               
                    data['both_color'] = 'bg-gray-100'
                    data['home_color'] = 'bg-blue-100 text-blue-700'
                    data['office_color'] = 'bg-gray-100'
                elif kwargs['type_filter'] == 'office':
                    data['both_color'] = 'bg-gray-100'
                    data['home_color'] = 'bg-gray-100'
                    data['office_color'] = 'bg-blue-100 text-blue-700'
                

        attendance_state = request.env.user.employee_id.attendance_state
        employee = request.env.user.employee_id


        
        data['attendance_state'] = attendance_state
        data['previous_attendance_change_date'] = employee.last_attendance_id and (employee.last_attendance_id.check_out or employee.last_attendance_id.check_in) or False
        data['employee_name'] = (employee.first_name + ' ' + employee.last_name) if (employee.first_name and employee.last_name) else employee.name
        data['hours_today'] = (datetime.now() - employee.permission_datetime).seconds if employee.has_permission else (employee.hours_today * 3600)
        # data['show_total_overtime'] = employee.company_id.hr_attendance_display_overtime
        data['total_overtime'] = employee.total_overtime
        data['overtime_today'] = request.env['hr.attendance.overtime'].sudo().search([
            ('employee_id', '=', employee.id), ('date', '=', fields.Date.context_today(request.env.user.employee_id)), ('adjustment', '=', False)]).duration or 0



        attendance_ids = request.env['hr.attendance'].with_user(SUPERUSER_ID).search(attendance_domain)

        if len(attendance_ids) > 0:
            absent_employees += attendance_ids.mapped('employee_id.id')

            for attendance in attendance_ids:
                
                if attendance.employee_id.id not in current_employees:
                    current_employees[attendance.employee_id.id] = {
                        'id': attendance.id,
                        'location': attendance.attendance_location,
                        'employee': attendance.employee_id.first_name+' '+attendance.employee_id.last_name if (attendance.employee_id.first_name and attendance.employee_id.last_name) else attendance.employee_id.name,
                        'symbol': attendance.employee_id.name[0:2].upper(),
                        'checked_status': attendance.employee_id.attendance_state,
                        'employee_id': attendance.employee_id
                    }


        data['attendance'] = current_employees.values()
        data['checked_in_count'] = len(current_employees.values())

        leave = []        
        work_from_home_id = request.env.ref('objects_hr_portal.work_from_home_type_id').id
        leave_ids = request.env['hr.leave'].with_user(SUPERUSER_ID).search([('holiday_status_id','!=',work_from_home_id),('request_date_from','<=',formatted_date),('request_date_to','>=',formatted_date),('state','!=','refuse')])   #,('state','=','validate')

        if len(leave_ids) > 0:
            absent_employees += leave_ids.mapped('employee_id.id')
            leave = leave_ids.mapped(lambda leave: {
                'id': leave.id,
                'date_range': f"{leave.request_date_from.strftime('%b %d')} - {leave.request_date_to.strftime('%b %d')}, {leave.request_date_to.strftime('%Y')}",
                'employee': leave.employee_id.first_name+' '+leave.employee_id.last_name if (leave.employee_id.first_name and leave.employee_id.last_name) else leave.employee_id.name,
                'symbol': leave.employee_id.name[0:2].upper(),
                'employee_id': leave.employee_id
            })


        data['leave'] = leave
        tag_id =  request.env['hr.employee.category'].with_user(SUPERUSER_ID).search([('name','=','No-ATTENDANCE')],limit=1)
        absent_ids = request.env['hr.employee'].with_user(SUPERUSER_ID).search([('id','not in',absent_employees),('category_ids','!=',tag_id.id)])

        if len(absent_ids) > 0:
            absents = absent_ids.mapped(lambda absent: {
                'id': absent.id,
                'name': absent.first_name+' '+absent.last_name if (absent.first_name and absent.last_name) else absent.name,
                'symbol': absent.name[0:2].upper(),
                'employee_id': absent
            })
        
        data['absent'] = absents


        pre_request_id = request.env['pre.leave.request'].with_user(SUPERUSER_ID).search([('manager_id','=',employee.id)],limit=1)
        pre_request_count = request.env['pre.leave.request'].with_user(SUPERUSER_ID).search_count([('manager_id','=',employee.id),('state','=','draft')])
        data['requests_visibility'] = '' if pre_request_id else 'hidden'
        data['pre_request_count'] = pre_request_count
        data['employee'] = employee
        data['has_permission'] = employee.has_permission
        data['permission_style'] = 'w-full justify-center mt-3' if employee.has_permission else ''




        # today = date.today()
        # target_date = datetime(2025, 6, 26).date()

        # if today >= target_date:        
        #     if today.day >= 26:
        #         # Go back one month
        #         first_day = (today.replace(day=1) - timedelta(days=1)).replace(day=26)
        #         last_day = today.replace(day=25)
        #     else:
        #         first_day = today.replace(day=26)
        #         # Go to next month
        #         next_month = today.replace(day=28) + timedelta(days=4)  # move to next month
        #         last_day = next_month.replace(day=25)
        #     # String versions
        #     first_day_str = first_day.strftime('%Y-%m-%d')
        #     last_day_str = last_day.strftime('%Y-%m-%d')
        #     leave_type = request.env.ref('objects_hr_portal.work_from_home_type_id').with_user(SUPERUSER_ID)
        #     allocated =(employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(first_day_str, "%Y-%m-%d").date(),datetime.strptime(last_day_str, "%Y-%m-%d").date()))[0]
        #     taken = (employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(first_day_str, "%Y-%m-%d").date(),datetime.strptime(last_day_str, "%Y-%m-%d").date()))[1]                  
        #     attendance_count = request.env['hr.attendance'].with_user(SUPERUSER_ID).search_count([('employee_id','=',employee.id),('check_in','>=',f"{formatted_date} 00:00"),('check_in','<=',f"{formatted_date} 23:59")])

        #     if taken == allocated and attendance_count == 0:
        #         data['disable_home'] = True
        #     else:
        #         data['disable_home'] = False
        
        # x_forwarded_for = request.httprequest.headers.get('X-Forwarded-For')
        # if x_forwarded_for:
        #     ip = x_forwarded_for.split(',')[0].strip()
        # else:
        #     ip = request.httprequest.remote_addr
        
        # data['ip'] = ip

        return request.render('objects_hr_portal.objects_home_portal_id',data)
    


    @http.route(['/objects/hr/check-in-out'], type='http', auth='user', website=True,methods=['POST'],csrf=False)
    def check_in(self, **kwargs):
      try:
        
          user = request.env.user
          employee = user.employee_id
          attendance_state = employee.attendance_state
          if 'feedback' not in kwargs and 'permission-check-in' not in kwargs and 'permission-check-out' not in kwargs:
                if attendance_state == 'checked_in':
                  return request.render('objects_hr_portal.objects_error_portal_id',{'error': 'You have Already Checked In'})

          if 'feedback' in kwargs:
                if attendance_state != 'checked_in':
                  return request.render('objects_hr_portal.objects_error_portal_id',{'error': 'You have Already Checked Out'})


          if 'permission-check-in' in kwargs:
                if attendance_state == 'checked_in':
                  return request.render('objects_hr_portal.objects_error_portal_id',{'error': 'You have Already Checked In'})

          if 'permission-check-out' in kwargs:
                if attendance_state != 'checked_in':
                  return request.render('objects_hr_portal.objects_error_portal_id',{'error': 'You have Already Checked Out'})

          today = date.today()
          today_str = today.strftime('%Y-%m-%d')
          time_zone = pytz.timezone(user.tz or 'UTC')
          current_dt = datetime.now()
          current_time = current_dt.time()
          tz_current_time = datetime.now(time_zone)
          attendance_config = request.env['attendance.conf'].with_user(SUPERUSER_ID).search([],limit=1)
          ten_am = time(attendance_config.maximum_check_in_hour, 0)

          current_td = timedelta(hours=tz_current_time.hour, minutes=tz_current_time.minute, seconds=tz_current_time.second)
          ten_am_td = timedelta(hours=ten_am.hour, minutes=ten_am.minute, seconds=ten_am.second)

          # Subtract and get difference in hours
          diff_td = current_td - ten_am_td
          hours_diff = diff_td.total_seconds() / 3600

          employee = request.env.user.employee_id
          attendance_penality_count = request.env['hr.attendance'].with_user(SUPERUSER_ID).search_count([('employee_id','=',employee.id),('check_in','>=',f"{today_str} 00:00"),('check_in','<=',f"{today_str} 23:59")])

          if tz_current_time.time() > ten_am and attendance_penality_count == 0:
              penality_id = request.env['hr.penality'].with_user(SUPERUSER_ID).search([
                  ('employee_id','=',employee.id),('date','=',today_str)
              ])
              
              if not penality_id and 'feedback' not in kwargs and 'permission-check-in' not in kwargs and 'permission-check-out' not in kwargs:
                  request.env['hr.penality'].with_user(SUPERUSER_ID).create({
                      'employee_id': employee.id,
                      'date': today_str,
                      'check_in_date': current_dt.strftime('%Y-%m-%d %H:%M:%S'),
                      'penality_hours': round(hours_diff,2)
                  })


          ips = request.env['ip.conf'].with_user(SUPERUSER_ID).search([]).mapped('ip')

          x_forwarded_for = request.httprequest.headers.get('X-Forwarded-For')
          if x_forwarded_for:
              ip = x_forwarded_for.split(',')[0].strip()
          else:
              ip = request.httprequest.remote_addr

          if ip in ips:
              attendance = request.env.user.employee_id.portal_action_attendance_action_change()
              if 'feedback' not in kwargs and 'permission-check-in' not in kwargs and 'permission-check-out' not in kwargs:
                attendance.write({
                    'attendance_location': 'office',
                    'check_in_location': 'office',
                    'ip': ip
                })

              if 'permission-check-in' in kwargs:
                attendance.write({
                    'attendance_location': 'office',
                    'check_in_location': 'office',
                })

              if 'permission-check-out' in kwargs:
                attendance.write({
                    'attendance_location': 'office',
                    'check_in_location': 'office',
                })


              if 'feedback' in kwargs:
                  attendance.write({
                      'attendance_location': 'office',
                      'check_out_location': 'office',
                      'ip_out': ip
                  })
          else:
              
              today = date.today()
              if today.day < 26:
                  # Go back one month
                  first_day = (today.replace(day=1) - timedelta(days=1)).replace(day=26)
                  last_day = today.replace(day=25)
              else:
                  first_day = today.replace(day=26)
                  # Go to next month
                  next_month = today.replace(day=28) + timedelta(days=4)  # move to next month
                  last_day = next_month.replace(day=25)

              # String versions
              first_day_str = first_day.strftime('%Y-%m-%d')
              last_day_str = last_day.strftime('%Y-%m-%d')

              leave_type = request.env.ref('objects_hr_portal.work_from_home_type_id').with_user(SUPERUSER_ID)
              allocated =(employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(first_day_str, "%Y-%m-%d").date(),datetime.strptime(last_day_str, "%Y-%m-%d").date()))[0]
              taken = (employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(first_day_str, "%Y-%m-%d").date(),datetime.strptime(last_day_str, "%Y-%m-%d").date()))[1]                  
              
              today = date.today()
              today_str = today.strftime('%Y-%m-%d')
              target_date = datetime(2025, 6, 26).date()
              leave_type = request.env.ref('objects_hr_portal.work_from_home_type_id').with_user(SUPERUSER_ID)
              employee = request.env.user.employee_id
              attendance_count = request.env['hr.attendance'].with_user(SUPERUSER_ID).search_count([('employee_id','=',employee.id),('check_in','>=',f"{today_str} 00:00"),('check_in','<=',f"{today_str} 23:59")])
              if attendance_count == 0 and 'feedback' not in kwargs and 'permission-check-in' not in kwargs and 'permission-check-out' not in kwargs:
                  if allocated - taken == 0:
                      return f"<h3>You Don't have enough balance to work from Home :(</h3>"
                  leave_id = request.env['hr.leave'].with_user(SUPERUSER_ID).create({
                        'holiday_type': 'employee',
                        'employee_id': employee.id,
                        'holiday_status_id': leave_type.id,
                        'employee_ids': [(6,0,[employee.id])],
                        'request_date_from': today_str,
                        'request_date_to': today_str,
                        'date_from': today_str,
                        'date_to': today_str,
                        'name': "Work From Home!!",   
                        'number_of_days': 1                                       
                  })
                  leave_id.action_approve()
                  leave_id.action_validate()
              
              attendance = request.env.user.employee_id.portal_action_attendance_action_change()
              if 'feedback' not in kwargs and 'permission-check-in' not in kwargs and 'permission-check-out' not in kwargs:
                  attendance.write({
                      'attendance_location': 'home',
                      'check_in_location': 'home',
                      'ip': ip
                  })

              if 'permission-check-in' in kwargs:
                  attendance.write({
                      'attendance_location': 'home',
                      'check_in_location': 'home',
                  })

              if 'permission-check-out' in kwargs:
                  attendance.write({
                      'attendance_location': 'home',
                      'check_in_location': 'home',
                  })


              if 'feedback' in kwargs:
                  attendance.write({
                      'attendance_location': 'home',
                      'check_out_location': 'home',
                      'ip_out': ip
                  })

          # if 'checkInType' in kwargs:

          #     attendance.write({
          #         'attendance_location': kwargs['checkInType']
          #     })

          if 'feedback' in kwargs:
              attendance.write({
                  'summary': kwargs['feedback']
              })            

          if 'permission-check-out' in kwargs:
              request.env.user.employee_id.has_permission = True
              request.env.user.employee_id.permission_datetime = datetime.now()
              

          if 'permission-check-in' in kwargs:
              request.env.user.employee_id.has_permission = False
              request.env.user.employee_id.permission_datetime = datetime.now()

          return request.redirect('/objects/hr/home')
      except Exception as e:
          return f'<h1>{e}</h1>'    


    @http.route(['/objects/change/password'], type='http', auth='user', website=True,methods=['POST'],csrf=True)
    def change_password(self, **kwargs):

      pass_id = request.env['change.password.wizard'].with_user(SUPERUSER_ID).create({'user_ids': [(0,0,{'user_id': request.env.user.id, 'user_login': request.env.user.login,'new_passwd': kwargs['password']})]})
      pass_id.user_ids.change_password_button()
      return request.redirect('/web')


    @http.route(['/','/my','/my/home'], type='http', auth="user", website=True)
    def portal_my_redirect(self, **kw):
        return request.redirect('/objects/hr/home')
