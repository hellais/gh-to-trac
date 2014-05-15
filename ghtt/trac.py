import re
import requests


class Trac(object):
    def __init__(self, base_path):
        self.base_path = base_path
        self.session = requests.Session()

    def get_form_token(self, path):
        r = self.session.get(path)
        m = re.search('__FORM_TOKEN.+?value=\"([a-z0-9]+)',
                      r.content)
        return m.group(1)

    def login(self, user, password):
        self.session.auth = (user, password)
        path = self.base_path + '/login'
        token = self.get_form_token(path)
        r = self.session.post(path,
                              data={'user': user,
                                    'password': password,
                                    'referer': self.base_path,
                                    '__FORM_TOKEN': token})
        # print r.content
        assert r.status_code == 200

    def create_ticket(self,
                      summary,
                      description,
                      component,
                      milestone='',
                      keywords='',
                      priority='normal',
                      ticket_type='defect',
                      owner='< default >',
                      cc='',
                      version=''):

        path = self.base_path + '/newticket'
        token = self.get_form_token(path)
        data = {
            'field_summary': summary,
            'field_description': description,
            'field_type': ticket_type,
            'field_priority': priority,
            'field_milestone': milestone,
            'field_component': component,
            'field_version': version,
            'field_keywords': keywords,
            'field_cc': cc,
            'field_actualpoints': '',
            'field_parent': '',
            'field_points': '',
            'field_owner': owner,
            'sfp_email': '',
            'sfph_mail': '',
            'submit': 'Create ticket',
            '__FORM_TOKEN': token
        }
        r = self.session.post(path, data=data)
        assert r.status_code == 200
