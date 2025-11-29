from odoo import http,SUPERUSER_ID,fields
from odoo.http import request
from odoo.tools import format_datetime
from datetime import date, timedelta,datetime
import pytz
from collections import defaultdict
from odoo.tools import format_datetime
import uuid
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)

class Attendance(http.Controller):


    def float_to_time(self,f):
        hours = int(f)
        minutes = int((f - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"

    def float_to_hours(self,f):
        hours = int(f)
        return f"{hours:2d}"


    @http.route(['/objects/compliance/create'], type='json', auth='public', website=True)
    def none_compliance(self,**kwargs):
        record_id = request.env['none.compliences'].with_user(SUPERUSER_ID).create({
                  "employee_id": kwargs['employee_id'],
                  "description": kwargs['description'],
                  "title": kwargs['title']
          })
        
        return {
            "status": "SUCCESS",
            "id": record_id.id
        }

    @http.route(['/objects/hr/attendance'], type='http', auth='user', website=True)
    def attendance(self, **kwargs):

        data = []        
        data_list = []
        holiday_hours = 0
        current_holiday_hours = 0
        current_leaves=0
        office_hours = 0
        home_hours = 0
        worked_hours = 0
        penalities = 0
        entries = []

        user_tz = request.env.user.tz or 'UTC'
        timezone = pytz.timezone(user_tz)
        employee = request.env.user.employee_id
        

        # today = date.today()
        # first_day = today.replace(day=1)
        # next_month = today.replace(day=28) + timedelta(days=4)  # this always pushes into the next month
        # last_day = next_month.replace(day=1) - timedelta(days=1)
        # first_day_str = first_day.strftime('%Y-%m-%d')
        # last_day_str = last_day.strftime('%Y-%m-%d')
        # count_fri_sat = sum(1 for i in range((today - first_day).days + 1) if (first_day + timedelta(days=i)).weekday() in (4, 5))
        # count_fri_sat_per_month = sum(1 for i in range(((first_day.replace(month=first_day.month % 12 + 1, day=1) - timedelta(days=1)) - first_day).days + 1) if (first_day + timedelta(days=i)).weekday() in (4, 5))
        # total_month_days = ((first_day.replace(month=first_day.month % 12 + 1, day=1) - timedelta(days=1)) - first_day).days + 1




        today = date.today()
        if today.day >= 26:
            current_filter = (today + relativedelta(months=1)).strftime('%m-%Y')
        else:
            current_filter = today.strftime('%m-%Y')

        # Determine if today is before the 26th — shift to previous month as "custom current month"
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

        # Fridays and Saturdays from first_day to today
        count_fri_sat = sum(
            1 for i in range((today - first_day).days + 1)
            if (first_day + timedelta(days=i)).weekday() in (4, 5)
        )

        # Fridays and Saturdays in the full custom month
        count_fri_sat_per_month = sum(
            1 for i in range((last_day - first_day).days + 1)
            if (first_day + timedelta(days=i)).weekday() in (4, 5)
        )

        # Total number of days in the custom month
        total_month_days = (last_day - first_day).days + 1







        # total_hours = request.env.user.employee_id.resource_calendar_id.hours_per_day * (total_month_days - count_fri_sat_per_month)
        # total_required_hours = request.env.user.employee_id.resource_calendar_id.hours_per_day * (today.day - count_fri_sat)

        hours_per_day = request.env.user.employee_id.resource_calendar_id.hours_per_day
        total_hours = hours_per_day * (total_month_days - count_fri_sat_per_month)
        total_required_hours = hours_per_day * ((today - first_day).days + 1 - count_fri_sat)
        


        if 'start' in kwargs and 'end' in kwargs:
              first_day_str = datetime.strptime(kwargs['start'], '%Y-%m-%d').date().strftime('%Y-%m-%d')
              last_day_str = datetime.strptime(kwargs['end'], '%Y-%m-%d').date().strftime('%Y-%m-%d')
              current_filter = datetime.strptime(kwargs['end'], '%Y-%m-%d').date().strftime('%m-%Y')                                


        attendance_ids = request.env['hr.attendance'].with_user(SUPERUSER_ID).search([('check_in','>=',first_day_str),('check_in','<=',last_day_str),('employee_id','=',request.env.user.employee_id.id)])
        
        if len(attendance_ids) > 0:

            office_hours = sum(attendance_ids.filtered(lambda att: att.attendance_location == 'office').mapped('worked_hours'))
            home_hours = sum(attendance_ids.filtered(lambda att: att.attendance_location == 'home').mapped('worked_hours'))
            worked_hours = sum(attendance_ids.mapped('worked_hours'))

            # data = attendance_ids.mapped(lambda attendance: {
            #     'id': attendance.id,
            #     'date': format_datetime(request.env, attendance.check_in, dt_format="MMM dd, yyyy"),
            #     'location': attendance.attendance_location,
            #     'in_time': fields.Datetime.from_string(attendance.check_in).astimezone(timezone).strftime('%H:%M') ,#attendance.check_in.strftime('%H:%M'),
            #     'out_time':  fields.Datetime.from_string(attendance.check_out).astimezone(timezone).strftime('%H:%M') if attendance.check_out else '',  #attendance.check_out.strftime('%H:%M') if attendance.check_out else '',
            #     'hours': round(attendance.worked_hours,2)
            # })


            grouped_data = defaultdict(list)

            # Group by local date (timezone-aware)
            for att in attendance_ids:
                check_in_local = fields.Datetime.from_string(att.check_in).astimezone(timezone)
                check_in_date = check_in_local.date()
                grouped_data[check_in_date].append(att)

            # Build grouped result
            for now_date, records in grouped_data.items():
                min_check_in = min(r.check_in for r in records)
                max_check_out = max((r.check_out for r in records if r.check_out), default=None)

                local_min = fields.Datetime.from_string(min_check_in).astimezone(timezone)
                local_max = fields.Datetime.from_string(max_check_out).astimezone(timezone) if max_check_out else None

                local_date = format_datetime(request.env, min_check_in, dt_format="MMM dd, yyyy")
                current_date = format_datetime(request.env, min_check_in, dt_format="YYYY-MM-dd")
                in_time = fields.Datetime.from_string(min_check_in).astimezone(timezone).strftime('%H:%M')
                out_time = (
                    fields.Datetime.from_string(max_check_out).astimezone(timezone).strftime('%H:%M')
                    if max_check_out else ''
                )
                total_hours_group = round(sum(r.worked_hours for r in records), 2)
                work_from_home_id = request.env.ref('objects_hr_portal.work_from_home_type_id').id    
                today_work_from_home_id = request.env['hr.leave'].with_user(SUPERUSER_ID).search([('employee_id','=',request.env.user.employee_id.id),('holiday_status_id','=', work_from_home_id),('request_date_from','<=',current_date),('request_date_to','>=',current_date),('state','=','validate')],order="create_date desc",limit=1)
                penality_ids = request.env['hr.penality'].with_user(SUPERUSER_ID).search([('employee_id','=',employee.id),('date','>=',current_date),('date','<=',current_date)])

                break_hours = 0
                if local_max:
                    span_hours = (local_max - local_min).total_seconds() / 3600
                    break_hours = round(span_hours - total_hours_group, 2)
                
                data_list.append({
                    'id': str(uuid.uuid4()),
                    'date': local_date,
                    'in_time': in_time,
                    'out_time': out_time,
                    'hours': self.float_to_time(total_hours_group),
                    'current_date': current_date,
                    'break_hours': self.float_to_time(break_hours),
                    'penality': self.float_to_time(sum(penality_ids.mapped('penality_hours'))),
                    'location': 'home' if today_work_from_home_id else 'office'
                })



        holiday_ids = request.env['resource.calendar.leaves'].with_user(SUPERUSER_ID).search([('resource_id', '=', False),('date_from','>=',first_day_str),('date_to','<=',last_day_str)])
        current_holiday_ids = request.env['resource.calendar.leaves'].with_user(SUPERUSER_ID).search([('resource_id', '=', False),('date_from','>=',first_day_str),('date_to','<=',today.strftime('%Y-%m-%d'))])

        zain_tag_id = request.env['hr.employee.category'].with_user(SUPERUSER_ID).search([('name','=','Zain')],limit=1)

        employee_leave_ids = request.env['hr.leave'].with_user(SUPERUSER_ID).search([
                    ('employee_id','=',request.env.user.employee_id.id),
                    ('holiday_status_id','!=', request.env.ref('objects_hr_portal.work_from_home_type_id').id),
                    ('request_date_from','>=',first_day_str),
                    ('request_date_to','<=',today.strftime('%Y-%m-%d')),
                    ('state','=','validate')],order="create_date desc",limit=1)

        if len(employee_leave_ids) > 0:
            current_leaves += float(sum(employee_leave_ids.mapped('number_of_days'))) * float(hours_per_day)

        # if len(current_holiday_ids) > 0:
        #     total_sum = sum(current_holiday_ids.mapped(lambda h: (h.date_to - h.date_from).days)) * hours_per_day
        #     current_holiday_hours += (hours_per_day if total_sum == 0 else total_sum)

        if len(current_holiday_ids) > 0 and zain_tag_id.id not in employee.category_ids.mapped('id'):
            for h in current_holiday_ids:
              total_sum = sum(h.mapped(lambda h: (h.date_to - h.date_from).days)) * hours_per_day
              current_holiday_hours += (hours_per_day if total_sum == 0 else total_sum)


        if len(holiday_ids) > 0 and zain_tag_id.id not in employee.category_ids.mapped('id'):
            for ho in holiday_ids:
              holidays_sum = sum(ho.mapped(lambda h: (h.date_to - h.date_from).days)) * hours_per_day
              holiday_hours += (hours_per_day if holidays_sum == 0 else holidays_sum)          

        penality_ids = request.env['hr.penality'].with_user(SUPERUSER_ID).search([('employee_id','=',employee.id),('date','>=',first_day_str),('date','<=',last_day_str)])

        if len(penality_ids) > 0:
            penalities = sum(penality_ids.mapped('penality_hours'))


        leave_type_ids = [request.env.ref('objects_hr_portal.work_from_home_type_id').with_user(SUPERUSER_ID)]


        for leave_type in leave_type_ids:

            vals = {'id': 0,'allocated': 0,'taken': 0, 'rest': 0,'name': ''}

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


            allocated =(employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(first_day_str, "%Y-%m-%d").date(),datetime.strptime(last_day_str, "%Y-%m-%d").date()))[0]
            taken = (employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(first_day_str, "%Y-%m-%d").date(),datetime.strptime(last_day_str, "%Y-%m-%d").date()))[1]                  
        
            vals['id'] = leave_type.id
            vals['name'] = leave_type.name
            vals['allocated'] = allocated if type(allocated) == float else 0.0
            vals['taken'] = taken if type(taken) == float else 0.0
            vals['rest'] = allocated - taken if (type(allocated) == float and type(taken) == float) else 0.0

            

            entries.append(vals)

        hours_req_difference = (total_required_hours - current_leaves) if zain_tag_id.id in employee.category_ids.mapped('id') else (total_required_hours - current_holiday_hours - current_leaves)

        if hours_req_difference < 0 :
            hours_req_difference = 0
        
        return request.render('objects_hr_portal.objects_attendance_portal_id',{
             'attendances': data_list,
             'office_hours': self.float_to_time(office_hours),
             'home_hours': self.float_to_time(home_hours),
             'office_float': office_hours,
             'home_float': home_hours,             
             'holiday_hours': holiday_hours,

             'worked_hours': self.float_to_hours(worked_hours),
             'required_hours': self.float_to_hours(total_required_hours - current_leaves) if zain_tag_id.id in employee.category_ids.mapped('id') else self.float_to_hours(total_required_hours - current_holiday_hours - current_leaves),
             'total_hours': self.float_to_hours(total_hours - holiday_hours),

             'worked_hours_float': worked_hours,
             'required_hours_float': (total_required_hours - current_leaves) if zain_tag_id.id in employee.category_ids.mapped('id') else (total_required_hours - current_holiday_hours - current_leaves),
             'total_hours_float': total_hours - holiday_hours,

             'current_filter': current_filter,
             'penalities': self.float_to_time(penalities),
             'entries': entries,

             'worked_required_diff_float': hours_req_difference - worked_hours,
             'worked_required_diff': self.float_to_time(hours_req_difference - worked_hours),
             'total_req': self.float_to_time(penalities + (hours_req_difference - worked_hours)) if (penalities + (hours_req_difference - worked_hours)) > 0 else self.float_to_time(0),

              'worked_hours_time': self.float_to_time(worked_hours),
              'required_hours_time': self.float_to_time(total_required_hours - current_leaves) if zain_tag_id.id in employee.category_ids.mapped('id') else self.float_to_time(total_required_hours - current_holiday_hours - current_leaves)

        })




    @http.route(['/objects/attendance/myrequests'], type='http', auth='user', website=True)
    def my_attendance_request(self, **kwargs):
        data = []        
        notification_ids = request.env['hr.notification'].with_user(SUPERUSER_ID).search([('employee_id','=',request.env.user.employee_id.id)],order="create_date desc")

        if len(notification_ids) > 0:
            data = notification_ids.mapped(lambda notification: {
                'id': notification.id,
                'in_time': self.convert_date_to_utc(notification.check_in.strftime('%Y-%m-%d %H:%M')) if notification.check_in else '',
                'out_time': self.convert_date_to_utc(notification.check_out.strftime('%Y-%m-%d %H:%M')) if notification.check_out else '',
                'message': notification.message,
                'state': notification.state[0].upper()+notification.state[1:],
                'employee': notification.employee_id.name,
            })

        return request.render('objects_hr_portal.objects_myrequests_portal_id',{'notifications': data})




    @http.route(['/objects/attendance/notification/create/view'], type='http', auth='user', website=True)
    def create_attendance_request(self, **kwargs):
        return request.render('objects_hr_portal.objects_notification_create_view_portal_id')



    def convert_date_to_utc(self,dt_str):
        utc_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
        utc_dt = pytz.utc.localize(utc_dt)
        user_tz = pytz.timezone(request.env.user.tz or 'UTC')
        local_dt = utc_dt.astimezone(user_tz)

        return local_dt.strftime("%H:%M")

    def convert_time_to_utc(self,dt_str):
          # Step 1: Parse the string into a naive datetime object
          local_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")

          # Step 2: Localize it to your local timezone (e.g., Egypt is UTC+3)
          local_tz = pytz.timezone(request.env.user.tz)
          localized_dt = local_tz.localize(local_dt)

          # Step 3: Convert it to UTC
          utc_dt = localized_dt.astimezone(pytz.utc)

          # Step 4: Convert it back to string
          utc_str = utc_dt.strftime("%Y-%m-%d %H:%M")        

          return utc_str

    @http.route(['/objects/attendance/notification/create'], type='http', auth='user', website=True,csrf=False)
    def action_create_attendance_request(self, **kwargs):
            vals = {
                'employee_id': request.env.user.employee_id.id,
                'check_in': self.convert_time_to_utc(kwargs['check_in'].replace('T',' ')),
                'message': kwargs['message'],
                'request_type': kwargs['attendance_categ']
            }

            if 'check_out' in kwargs:
                if kwargs['check_out']:
                  vals['check_out'] = self.convert_time_to_utc(kwargs['check_out'].replace('T',' '))

            if 'location' in kwargs:
                vals['attendance_location'] = kwargs['location']

            request.env['hr.notification'].with_user(SUPERUSER_ID).create(vals)

            return request.redirect('/objects/attendance/myrequests')
