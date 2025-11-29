from odoo import http,SUPERUSER_ID
from odoo.http import request
from odoo.tools import format_datetime
from datetime import date, timedelta

class Assignment(http.Controller):


    @http.route(['/objects/hr/assignments'], type='http', auth='user', website=True)
    def attendance(self, **kwargs):

        assignments = []
        employee = request.env.user.employee_id

        project_ids = request.env['project.team.members'].with_user(SUPERUSER_ID).search([('employee_id','=',employee.id)],order='date_to desc, date_from desc')

        if len(project_ids) > 0:
            for project in project_ids:
                assignments.append({
                    'id': project.id,
                    'project': project.project_id.name,
                    'from': project.date_from,
                    'to': project.date_to,
                    'utilization': project.utilization
                })  

        return request.render('objects_hr_portal.objects_assignments_portal_id',{'assignments': assignments})
