# -*- coding: utf-8 -*-

from odoo import models, fields, api,SUPERUSER_ID
from odoo import models, fields, api, exceptions, _
import secrets
import string


class User(models.Model):
    _inherit = 'res.users'

    def change_pass_and_send_mail(self):
      alphabet = string.ascii_letters + string.digits
      new_password = ''.join(secrets.choice(alphabet) for i in range(20))
      pass_id = self.env['change.password.wizard'].with_user(SUPERUSER_ID).create({'user_ids': [(0,0,{'user_id': self.id, 'user_login': self.login,'new_passwd': new_password})]})
      pass_id.user_ids.change_password_button()
      mail_content = f""""
              <h3>Hello {self.name},</h3>
              <p>url: https://erp.objects.ws/</p>
              <p>username: {self.login}</p>
              <p>password: {new_password}</p>
      """
      main_content = {
          'subject': f"Objects Username",
          'author_id': self.partner_id.id,
          'body_html': mail_content,
          'email_to': self.login,
      }
      self.env['mail.mail'].sudo().create(main_content).send()

