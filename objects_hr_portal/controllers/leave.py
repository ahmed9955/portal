from odoo import http,SUPERUSER_ID
from odoo.http import request
from datetime import datetime,date,timedelta
import json

class Leave(http.Controller):

    @http.route(['/objects/hr/leave'], type='http', auth='user', website=True)
    def leave(self, **kwargs):

        data = []        
        entries = []
        entries_per_month = {}

        work_from_home_id = request.env.ref('objects_hr_portal.work_from_home_type_id').id    
        leave_ids = request.env['hr.leave'].with_user(SUPERUSER_ID).search([('employee_id','=',request.env.user.employee_id.id),('holiday_status_id','!=', work_from_home_id)],order="create_date desc")
        leave_type_ids = [request.env.ref('objects_hr_portal.anuual_leave_type_id').with_user(SUPERUSER_ID),request.env.ref('objects_hr_portal.compensatory_leave_type_id').with_user(SUPERUSER_ID)] #request.env['hr.leave.type'].with_user(SUPERUSER_ID).search([])
        employee = request.env.user.employee_id


        

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



            allocated =(employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(f'{date.today().year}-01-01', "%Y-%m-%d").date(),datetime.strptime(f'{date.today().year}-12-31', "%Y-%m-%d").date()))[0]
            taken = (employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(f'{date.today().year}-01-01', "%Y-%m-%d").date(),datetime.strptime(f'{date.today().year}-12-31', "%Y-%m-%d").date()))[1]                  
            rest = (employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(f'{date.today().year}-01-01', "%Y-%m-%d").date(),datetime.strptime(f'{date.today().year}-12-31', "%Y-%m-%d").date()))[2]

            # allocated =(employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(first_day_str, "%Y-%m-%d").date(),datetime.strptime(last_day_str, "%Y-%m-%d").date()))[0]
            # taken = (employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(first_day_str, "%Y-%m-%d").date(),datetime.strptime(last_day_str, "%Y-%m-%d").date()))[1]                  
            # rest = (employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(first_day_str, "%Y-%m-%d").date(),datetime.strptime(last_day_str, "%Y-%m-%d").date()))[2]

            vals['id'] = leave_type.id
            vals['name'] = leave_type.name
            vals['allocated'] = allocated if type(allocated) == float else 0.0
            vals['taken'] = taken if type(taken) == float else 0.0
            vals['rest'] = allocated - taken if (type(allocated) == float and type(taken) == float) else 0.0

            

            entries.append(vals)


            chart_taken_jan =(employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(f'{date.today().year}-01-01', "%Y-%m-%d").date(),datetime.strptime(f'{date.today().year}-02-01', "%Y-%m-%d").date()))[1] 
            chart_taken_feb =(employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(f'{date.today().year}-02-01', "%Y-%m-%d").date(),datetime.strptime(f'{date.today().year}-03-01', "%Y-%m-%d").date()))[1] 
            chart_taken_mar =(employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(f'{date.today().year}-03-01', "%Y-%m-%d").date(),datetime.strptime(f'{date.today().year}-04-01', "%Y-%m-%d").date()))[1] 
            chart_taken_apr =(employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(f'{date.today().year}-04-01', "%Y-%m-%d").date(),datetime.strptime(f'{date.today().year}-05-01', "%Y-%m-%d").date()))[1] 
            chart_taken_may =(employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(f'{date.today().year}-05-01', "%Y-%m-%d").date(),datetime.strptime(f'{date.today().year}-06-01', "%Y-%m-%d").date()))[1] 
            chart_taken_jun =(employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(f'{date.today().year}-06-01', "%Y-%m-%d").date(),datetime.strptime(f'{date.today().year}-07-01', "%Y-%m-%d").date()))[1] 
            chart_taken_jul =(employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(f'{date.today().year}-07-01', "%Y-%m-%d").date(),datetime.strptime(f'{date.today().year}-08-01', "%Y-%m-%d").date()))[1] 
            chart_taken_aug =(employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(f'{date.today().year}-08-01', "%Y-%m-%d").date(),datetime.strptime(f'{date.today().year}-09-01', "%Y-%m-%d").date()))[1] 
            chart_taken_sep =(employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(f'{date.today().year}-09-01', "%Y-%m-%d").date(),datetime.strptime(f'{date.today().year}-10-01', "%Y-%m-%d").date()))[1] 
            chart_taken_oct =(employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(f'{date.today().year}-10-01', "%Y-%m-%d").date(),datetime.strptime(f'{date.today().year}-11-01', "%Y-%m-%d").date()))[1] 
            chart_taken_nov =(employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(f'{date.today().year}-11-01', "%Y-%m-%d").date(),datetime.strptime(f'{date.today().year}-12-01', "%Y-%m-%d").date()))[1] 
            chart_taken_dec =(employee.count_employee_leave_allocation_rest_taken_by_date_and_type(leave_type,datetime.strptime(f'{date.today().year}-12-01', "%Y-%m-%d").date(),datetime.strptime(f'{date.today().year+1}-01-01', "%Y-%m-%d").date()))[1] 




            if leave_type.id == request.env.ref('objects_hr_portal.anuual_leave_type_id').id:
                

                entries_per_month['annual'] = [
                    chart_taken_jan if type(chart_taken_jan) == float else 0.0 ,
                    chart_taken_feb if type(chart_taken_feb) == float else 0.0 ,
                    chart_taken_mar if type(chart_taken_mar) == float else 0.0 ,
                    chart_taken_apr if type(chart_taken_apr) == float else 0.0 ,
                    chart_taken_may if type(chart_taken_may) == float else 0.0 ,
                    chart_taken_jun if type(chart_taken_jun) == float else 0.0 ,
                    chart_taken_jul if type(chart_taken_jul) == float else 0.0 ,
                    chart_taken_aug if type(chart_taken_aug) == float else 0.0 ,
                    chart_taken_sep if type(chart_taken_sep) == float else 0.0 ,
                    chart_taken_oct if type(chart_taken_oct) == float else 0.0 ,
                    chart_taken_nov if type(chart_taken_nov) == float else 0.0 ,
                    chart_taken_dec if type(chart_taken_dec) == float else 0.0 
                ]

            if leave_type.id == request.env.ref('objects_hr_portal.compensatory_leave_type_id').id:
                entries_per_month['compensatory'] =  [
                    chart_taken_jan if type(chart_taken_jan) == float else 0.0 ,
                    chart_taken_feb if type(chart_taken_feb) == float else 0.0 ,
                    chart_taken_mar if type(chart_taken_mar) == float else 0.0 ,
                    chart_taken_apr if type(chart_taken_apr) == float else 0.0 ,
                    chart_taken_may if type(chart_taken_may) == float else 0.0 ,
                    chart_taken_jun if type(chart_taken_jun) == float else 0.0 ,
                    chart_taken_jul if type(chart_taken_jul) == float else 0.0 ,
                    chart_taken_aug if type(chart_taken_aug) == float else 0.0 ,
                    chart_taken_sep if type(chart_taken_sep) == float else 0.0 ,
                    chart_taken_oct if type(chart_taken_oct) == float else 0.0 ,
                    chart_taken_nov if type(chart_taken_nov) == float else 0.0 ,
                    chart_taken_dec if type(chart_taken_dec) == float else 0.0 
                ]

            if leave_type.id == request.env.ref('objects_hr_portal.work_from_home_type_id').id:
                entries_per_month['home'] = [
                    chart_taken_jan if type(chart_taken_jan) == float else 0.0 ,
                    chart_taken_feb if type(chart_taken_feb) == float else 0.0 ,
                    chart_taken_mar if type(chart_taken_mar) == float else 0.0 ,
                    chart_taken_apr if type(chart_taken_apr) == float else 0.0 ,
                    chart_taken_may if type(chart_taken_may) == float else 0.0 ,
                    chart_taken_jun if type(chart_taken_jun) == float else 0.0 ,
                    chart_taken_jul if type(chart_taken_jul) == float else 0.0 ,
                    chart_taken_aug if type(chart_taken_aug) == float else 0.0 ,
                    chart_taken_sep if type(chart_taken_sep) == float else 0.0 ,
                    chart_taken_oct if type(chart_taken_oct) == float else 0.0 ,
                    chart_taken_nov if type(chart_taken_nov) == float else 0.0 ,
                    chart_taken_dec if type(chart_taken_dec) == float else 0.0 
                ]



        if len(leave_ids) > 0:
            data = leave_ids.mapped(lambda leave: {
                'id': leave.id,
                'type': leave.holiday_status_id.name,
                'start_date': leave.request_date_from,
                'end_date': leave.request_date_to,
                # 'days': (leave.request_date_to - leave.request_date_from).days,
                'days': float(leave.number_of_days),
                'state': dict(leave._fields['state'].selection).get(leave.state)
            })
        
        return request.render('objects_hr_portal.objects_leave_portal_id',{'leaves': data,'entries': entries,'entries_per_month': json.dumps(entries_per_month)})
    

    @http.route(['/objects/leave/create/view'], type='http', auth='user', website=True)
    def create_leave_request(self, **kwargs):
        # leave_types = request.env['hr.leave.type'].with_user(SUPERUSER_ID).search([
        #     '|',
        #     ('requires_allocation','=','no'),
        #     '&',
        #     ('has_valid_allocation','=',True),
        #     '|',
        #     ('allows_negative','=',True),
        #     '&',
        #     ('virtual_remaining_leaves','>',0),
        #     ('allows_negative','=',False)
        # ]).mapped(lambda type:{'id': type.id,'name': type.name})

        leave_types = request.env['hr.leave.type'].with_user(SUPERUSER_ID).browse([
            request.env.ref('objects_hr_portal.anuual_leave_type_id').with_user(SUPERUSER_ID).id,
            request.env.ref('objects_hr_portal.compensatory_leave_type_id').with_user(SUPERUSER_ID).id
        ]).mapped(lambda type:{'id': type.id,'name': type.name})

            # request.env.ref('objects_hr_portal.work_from_home_type_id').with_user(SUPERUSER_ID).id

        return request.render('objects_hr_portal.objects_leave_create_view_portal_id',{'types': leave_types})


    def count_days_excluding_fri_sat(self,kwargs):
      check_in_date = datetime.strptime(kwargs['check_in'], '%Y-%m-%d').date()
      check_out_date = datetime.strptime(kwargs['check_out'], '%Y-%m-%d').date()
      
      current_date = check_in_date
      no_of_days = 0
      
      while current_date < check_out_date:
          # weekday() returns 0-6 (Monday-Sunday)
          # Friday = 4, Saturday = 5
          if current_date.weekday() not in [4, 5]:  # Exclude Friday and Saturday
              no_of_days += 1
          current_date += timedelta(days=1)
      
      return no_of_days

    @http.route(['/objects/leave/create'], type='http', auth='user', website=True,csrf=False)
    def action_create_leave_request(self, **kwargs):
            projects_vals = {}
            # no_of_days = (datetime.strptime(kwargs['check_out'], '%Y-%m-%d').date() - datetime.strptime(kwargs['check_in'], '%Y-%m-%d').date()).days
            no_of_days = self.count_days_excluding_fri_sat(kwargs)
            create_vals = {
                'employee_ids': [(6,0,[request.env.user.employee_id.id])],
                'employee_id': request.env.user.employee_id.id,
                'holiday_status_id': int(kwargs['type']),
                'request_date_from': kwargs['check_in'],
                'request_date_to': kwargs['check_out'],
                'date_from': kwargs['check_in']+' 00:00',
                'date_to': kwargs['check_out']+' 23:59',
                'name': kwargs['description'],
                'is_header_visible': False,
                'number_of_days': no_of_days + 1 
            }

            if 'half_day' in kwargs:
                create_vals['request_date_from'] = kwargs['check_in']
                create_vals['date_from'] = kwargs['check_in']
                create_vals['request_date_to'] = kwargs['check_in']
                create_vals['date_to'] = kwargs['check_in']
                create_vals['number_of_days'] = 0.5
                create_vals['request_unit_half'] = True


            employee = request.env.user.employee_id
            project_ids = request.env['project.project'].with_user(SUPERUSER_ID).search([
                ('project_team_member_ids.employee_id','=',employee.id),
                ('facilitator_id','!=',False),
                ('facilitator_id','!=',employee.id)
            ])
          
            if len(project_ids) > 0:
                prepared_vals = project_ids.mapped(lambda project:(0,0,{
                    'employee_id': employee.id,
                    'manager_id': project.facilitator_id.id,
                    'project_id': project.id,
                    'request_type': 'facilitator'
                }))
                projects = project_ids.filtered(lambda p: p.facilitator_id.id != p.user_id.employee_id.id and p.facilitator_id != False)
                for p in projects:
                    if p.user_id.employee_id.id not in projects_vals:
                        projects_vals[p.user_id.employee_id.id] = [(0,0,{
                                                                    'employee_id': employee.id,
                                                                    'manager_id': p.user_id.employee_id.id,
                                                                    'project_id': p.id,
                                                                    'request_type': 'manager'
                                                                  })]                                              
                # .mapped(lambda p:(0,0,{
                #     'employee_id': employee.id,
                #     'manager_id': p.user_id.employee_id.id,
                #     'project_id': p.id,
                #     'request_type': 'manager'
                # }))
                create_vals['pre_leave_request_ids'] = prepared_vals + list(projects_vals.values())[0]
            else:
                create_vals['is_header_visible'] = True

            request.env['hr.leave'].with_user(SUPERUSER_ID).create(create_vals)

            return request.redirect('/objects/hr/leave')

    def hide_buttons_method(self,request):
        is_all_approved = all(request.leave_id.pre_leave_request_ids.filtered(lambda l:l.id != request.id and l.request_type == 'facilitator').mapped(lambda r:r.state == 'approve'))        
        if request.request_type == 'manager' and is_all_approved:
            return 'f'
        elif request.request_type != 'manager':
            return 'f'
        else:
          return  't'

    @http.route(['/objects/hr/prerequests'], type='http', auth='user', website=True)
    def pre_request(self, **kwargs):
      data = {'prerequests': []}
      today = date.today()
      first_day = today.replace(day=1)
      next_month = today.replace(day=28) + timedelta(days=4)  # this always pushes into the next month
      last_day = next_month.replace(day=1) - timedelta(days=1)

      # ('create_date','>=',first_day.strftime('%Y-%m-%d')),
      # ('create_date','<=',last_day.strftime('%Y-%m-%d')),
      # ,('state','=','draft')
      
      employee = request.env.user.employee_id
      pre_request_ids = request.env['pre.leave.request'].with_user(SUPERUSER_ID).search([
          ('manager_id','=',employee.id)],order="create_date desc")

      if len(pre_request_ids) > 0:
        all_requests = []

        for req in pre_request_ids:
            # if req.request_type == 'manager':
            other_request_ids = req.leave_id.pre_leave_request_ids.filtered(lambda l:l.id != req.id and l.request_type != 'manager' and l.state != 'approve')
          
              # for other in other_request_ids:
              #     if other.id not in list(map(lambda r:r['id'],all_requests)):                  
              #           all_requests += [{
              #                                                       'id': other.id,            
              #                                                       'type': other.leave_id.holiday_status_id.name,
              #                                                       'start_date': other.leave_id.request_date_from,
              #                                                       'end_date': other.leave_id.request_date_to,
              #                                                       'days': (other.leave_id.request_date_to - other.leave_id.request_date_from).days,
              #                                                       'state': dict(other._fields['state'].selection).get(other.state),
              #                                                       'project': other.project_id.name,
              #                                                       'employee': other.employee_id.name,
              #                                                       'manager': other.manager_id.name,
              #                                                       'employee_id':  other.manager_id.id,
              #                                                       'current_employee_id': employee.id,
              #                                                       'hide': 't'

              #                                                     }]
            
            all_requests += req.mapped(lambda request: {
                                                          'id': request.id,            
                                                          'type': request.leave_id.holiday_status_id.name,
                                                          'start_date': request.leave_id.request_date_from,
                                                          'end_date': request.leave_id.request_date_to,
                                                          # 'days': (request.leave_id.request_date_to - request.leave_id.request_date_from).days,
                                                          'days': float(request.leave_id.number_of_days),
                                                          'state': dict(request._fields['state'].selection).get(request.state),
                                                          'project': request.project_id.name,
                                                          'employee': request.employee_id.name,
                                                          'manager': request.manager_id.name,
                                                          'employee_id':  request.manager_id.id,
                                                          'current_employee_id': employee.id,
                                                          'hide': self.hide_buttons_method(request),
                                                          'facitlitators': ' - '.join(other_request_ids.mapped(lambda r: r.manager_id.name)) if len(other_request_ids) > 0 else ''
                                                        })

        # prepared_vals = pre_request_ids.mapped(lambda request: {
        #   'id': request.id,            
        #   'type': request.leave_id.holiday_status_id.name,
        #   'start_date': request.leave_id.request_date_from,
        #   'end_date': request.leave_id.request_date_to,
        #   'days': (request.leave_id.request_date_to - request.leave_id.request_date_from).days,
        #   'state': dict(request._fields['state'].selection).get(request.state),
        #   'project': request.project_id.name,
        #   'employee': request.employee_id.name
        # })

        # pre_requests = pre_request_ids.filtered(lambda r:r.request_type == 'manager')
        
        # if len(pre_requests) > 0:
        #   for p in pre_requests:
        #       p.leave_id.
            
            
            


        data['prerequests'] = all_requests

      return request.render('objects_hr_portal.objects_pre_leave_request',data)
    

    @http.route(['/objects/submit/prerequest'], type='http', auth='user',methods=["POST"], website=True,csrf=False)
    def action_create_preleave_request(self, **kwargs):

      if 'id' in kwargs and 'type' in kwargs:
          request_id = request.env['pre.leave.request'].with_user(SUPERUSER_ID).browse(int(kwargs['id']))
          if kwargs['type'] == 'approve':
              request_id.with_user(SUPERUSER_ID).action_approve()
          else:
              request_id.with_user(SUPERUSER_ID).action_reject()              

      return request.redirect('/objects/hr/prerequests')
