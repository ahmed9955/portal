# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import models, fields, api, exceptions, _


class PreLeaveRequest(models.Model):
    _name = 'pre.leave.request'
    _description = 'Pre Leave Request'

    employee_id = fields.Many2one('hr.employee',string="Employee",required=True)
    manager_id = fields.Many2one('hr.employee',string="Manager",required=True)
    leave_id = fields.Many2one('hr.leave',string="Leave",required=True,ondelete="cascade")
    project_id = fields.Many2one('project.project',string="Project",required=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('refuse', 'Refused'),
                              ('approve','Approved')],string="Status",default='draft')
    request_type = fields.Selection([('manager', 'Manager'),
                                    ('facilitator', 'Facilitator')],string="Status",default='facilitator')

    def action_approve(self):
        
        all_request_approved = all(self.leave_id.pre_leave_request_ids.filtered(lambda req: req.id != self.id ).mapped(lambda request: request.state == 'approve'))

        if all_request_approved:
            if self.leave_id.state == 'confirm':
              self.leave_id.is_header_visible = True
              self.leave_id.action_draft()
              self.leave_id.action_confirm()

        self.state = 'approve'


    def action_reject(self):
        self.state = 'refuse'        
        self.leave_id.is_header_visible = False

        all_request_refused = all(self.leave_id.pre_leave_request_ids.filtered(lambda req: req.id != self.id ).mapped(lambda request: request.state == 'refuse'))

        if all_request_refused:
            self.leave_id.action_refuse()
