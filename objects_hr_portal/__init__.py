# -*- coding: utf-8 -*-

from . import controllers
from . import models
from odoo import api, SUPERUSER_ID


def _create_portal_pages_hook(cr,registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    page_ids = env['website.page'].with_user(SUPERUSER_ID).create([{
        'is_published': True,
        'url': '/objects/hr/attendance',
        'track': True,
        'view_id': env.ref('website.homepage').id,
        'website_meta_description': 'Attendance',
    },{
        'is_published': True,
        'url': '/objects/hr/leave',
        'track': True,
        'view_id': env.ref('website.homepage').id,
        'website_meta_description': 'Leave',        
    }])

    i = 11
    for page_id in page_ids:
        env['website.menu'].with_user(SUPERUSER_ID).create({
            'name': page_id.website_meta_description,
            'page_id': page_id.id,
            'parent_id': env.ref('website.main_menu').id,
            'sequence': i
        })

        i += 1


def _uninstall_module_hook(cr,registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['website.menu'].with_user(SUPERUSER_ID).search([('url','in',('/objects/hr/leave','/objects/hr/attendance'))]).unlink()    
    env['website.page'].with_user(SUPERUSER_ID).search([('url','in',('/objects/hr/leave','/objects/hr/attendance'))]).unlink()
    