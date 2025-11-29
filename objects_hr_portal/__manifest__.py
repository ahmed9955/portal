# -*- coding: utf-8 -*-
{
    'name': "objects_hr_portal",
    'summary': "",
    'description': """
    """,
    'author': "My Company",
    'website': "https://objects.ws/",
    'category': 'HR',
    'version': '0.1',
    'depends': [
                'base', 
                'portal', 
                'website',
                'hr',
                'hr_notifications',
                'hr_holidays',
                'calendar', 
                'mail',
                'project',
                'objects_project_team',
                'hr_attendance'
              ],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/hr_employee.xml',
        'views/templates.xml',
        'views/home.xml',
        'views/leave.xml',
        'views/attendance.xml',
        'views/leave_view.xml',
        'views/project.xml',
        'views/assignments.xml',
        'views/evaluation.xml',
        'views/penality.xml',
        'views/non_complience.xml'
    ],

    'assets': {
        'web.assets_frontend': [
            '/objects_hr_portal/static/src/css/style.css',
            '/objects_hr_portal/static/src/js/jshome.js',
            '/objects_hr_portal/static/src/js/jsattendance.js',
            '/objects_hr_portal/static/src/js/jsleave.js',
            '/objects_hr_portal/static/src/js/jsevaluation.js',
            '/objects_hr_portal/static/src/js/jsattendance_request.js'
        ],
    },

    'post_init_hook': '_create_portal_pages_hook',
    'uninstall_hook': '_uninstall_module_hook'

}