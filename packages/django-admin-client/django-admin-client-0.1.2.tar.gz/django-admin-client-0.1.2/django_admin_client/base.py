import copy
import json
import re

import requests
from bs4 import BeautifulSoup

from .exceptions import LoginFailed, NoMatches, MoreThanOneMatch, NotLoggedInOrSessionExpired, \
    DjangoAdminInvalidRequest, MissingRequiredArgument, PassedUnrecognizedArguments


class DjangoAdminBase:
    def __init__(self, base_url, superuser_email, superuser_password, session=None):
        self._base_url = base_url.rstrip('/')
        self._superuser_email = superuser_email
        self._superuser_password = superuser_password
        self._session = session

    @property
    def session(self):
        if not self._session:
            self._session = requests.Session()
        return self._session

    def close_session(self):
        if self._session:
            self._session.close()

    def login(self):
        path = '/login/'
        username = self._superuser_email
        password = self._superuser_password

        post_resp = self.post_with_csrf_and_auto_login(path, auto_login=False, data={
            'username': username,
            'password': password,
            'next': '/admin/'
        })['response']  # sessionid cookie is set on session after this step

        soup = BeautifulSoup(post_resp.text, features='html.parser')
        if soup.find(text=re.compile('Please enter the correct username and password')):
            raise LoginFailed(
                'Invalid username or password; url: {url}, username: {username}, password: {password}'.format(
                    url=self._base_url + path, username=username, password=password))
        return post_resp

    def get_with_auto_login(self, path, auto_login=True, **kwargs):
        url = self._base_url + path
        resp = self.session.get(url, **kwargs)
        if self._is_redirect_to_login(resp):
            if not auto_login:
                raise NotLoggedInOrSessionExpired('url: {url}'.format(url=url))
            self.login()
            return self.get_with_auto_login(path, auto_login=False, **kwargs)
        return resp

    def post_with_csrf_and_auto_login(self, path, data, auto_login=True, auto_csrf=True, raise_if_errors=False, **kwargs):
        url = self._base_url + path
        if auto_csrf:
            get_resp = self.get_with_auto_login(path, auto_login=auto_login)
            soup = BeautifulSoup(get_resp.text, features='html.parser')
            csrf = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
            data.update({'csrfmiddlewaretoken': csrf})

        post_resp = self.session.post(url, data=data, **kwargs)

        if self._is_redirect_to_login(post_resp):
            if not auto_login:
                raise NotLoggedInOrSessionExpired('url: {url}'.format(url=url))
            self.login()
            return self.post_with_csrf_and_auto_login(url, data, auto_login=False, auto_csrf=auto_csrf, raise_if_errors=raise_if_errors, **kwargs)

        soup = BeautifulSoup(post_resp.text, features='html.parser')
        errors = soup.find_all(attrs={'class': 'errors'})
        if errors and raise_if_errors:
            raise DjangoAdminInvalidRequest("url: '{url}', data: '{data}', errors: {errors}".format(url=url, data=data, errors=errors), response=post_resp, errors=errors)

        return {'response': post_resp, 'errors': errors}

    @staticmethod
    def _is_redirect_to_login(resp):
        result = False
        if (resp.history
                and resp.history[0].status_code == 302
                and resp.history[0].headers['location'].startswith('/admin/login/')):
            result = True

        return result

    @staticmethod
    def _try_inline_group(soup):
        fields = {}
        inline_group = soup.find('div', {'class': 'inline-group'})
        if not inline_group:
            return fields

        inline_fields_prefix = json.loads(inline_group['data-inline-formset'])['options']['prefix']
        tags = inline_group.find_all(attrs={'name': re.compile(inline_fields_prefix)})
        for tag in tags:
            field_name = tag['name']
            fields[field_name] = {
                "name": field_name,
                "required": False,  # todo: mark required once
                "default_value": tag.get('value', '')
            }

        return fields

    def generate_spec(self):
        models = {}

        r = self.get_with_auto_login('/')

        s = BeautifulSoup(r.text, features='html.parser')

        for row in s.find_all(attrs={'scope': 'row'}):
            # <th scope="row"><a href="/admin/auth/group/">Groups</a></th>

            model_id = "_".join(row.a.text.split()).lower()

            a_elements = row.a['href'].strip('/').split('/')
            model_app, model_name = a_elements[-2:]

            add_resp = self.get_with_auto_login("/{model_app}/{model_name}/add/".format(**locals()))
            s2 = BeautifulSoup(add_resp.text, features='html.parser')

            fields = {}
            field_labels = s2.find_all('label')
            for label in field_labels:
                field_name = label['for'][len('id_'):]
                fields[field_name] = {
                    "name": field_name,
                    "required": 'required' in label.get('class', []),
                    "default_value": label.get('value', '')
                }

            fields.update(self._try_inline_group(s2))

            models[model_id] = {
                "id": model_id,
                "app": model_app,
                "name": model_name,
                "fields": fields
            }

        return {'models': models}


class DjangoAdminModel:
    def __init__(self, django_admin: DjangoAdminBase, path: str, fields: dict = None):
        self._da = django_admin
        self._path = path
        self._fields = fields

    def all(self):
        resp = self._da.get_with_auto_login(self._path, params={'all': ''})
        soup = BeautifulSoup(resp.text, features='html.parser')
        table = soup.find('tbody')
        if table:
            ids = [input_tag['value'] for input_tag in table.find_all('input')]
        else:
            ids = []

        return {'_response': resp, 'ids': ids}

    def find(self, query):
        resp = self._da.get_with_auto_login(self._path, params={'all': ''})
        soup = BeautifulSoup(resp.text, features='html.parser')
        table = soup.find('tbody')
        if not table:
            raise NoMatches("There's no any object")

        matching_strings = table.find_all(text=re.compile(query))
        if not matching_strings:
            raise NoMatches("key: '{key}'".format(key=query))
        if len(matching_strings) > 1:
            raise MoreThanOneMatch("key: '{key}', result: {match}".format(key=query, match=matching_strings))

        matching_string = matching_strings[0]
        tr = matching_string.find_parent('tr')
        object_id = tr.find('input')['value']

        return {'_response': resp, 'id': object_id}

    def add(self, item):
        path = self._path.rstrip('/')

        add_path = path + '/add/'

        # prepare data
        if self._fields is None:
            data = item
        else:
            missing_required_fields = []
            item_copy = copy.deepcopy(item)

            data = copy.deepcopy(self._fields)
            for field_name, spec_field_attrs in self._fields.items():
                value = item_copy.pop(field_name, None)
                if value is not None:
                    data[field_name] = value
                else:
                    if spec_field_attrs['required']:
                        missing_required_fields.append(field_name)

                    elif spec_field_attrs['default_value'] is None:
                        del data[field_name]

            if missing_required_fields:
                raise MissingRequiredArgument(str(missing_required_fields))

            if item_copy:
                raise PassedUnrecognizedArguments(str(item_copy))

        data['_continue'] = 'Save and continue editing'
        # !prepare data

        try:
            resp = self._da.post_with_csrf_and_auto_login(add_path, data=data, raise_if_errors=True)
            response = resp['response']
            if not response.status_code == 200 or len(response.history) > 1:
                return {'_response': response, 'id': None, 'created': False}
            created = True
        except DjangoAdminInvalidRequest as exc:
            if (len(exc.errors) == 1
                    and 'already exists' in str(exc.errors[0])):
                response = exc.response
                created = False
            else:
                raise

        if created:
            match = re.search(path + r'/([^/]+)/change/', response.url)
            try:
                object_id = match.group(1)
            except AttributeError:
                object_id = None
        else:
            object_id = None

        return {'_response': response, 'id': object_id, 'created': created}

    def get(self, object_id):
        resp = self._da.get_with_auto_login('{path}{object_id}/change/'.format(path=self._path, object_id=object_id))
        soup = BeautifulSoup(resp.text, features='html.parser')
        form_rows = soup.find_all('div', {'class': 'form-row'})
        fields_dict = {}
        for form_row in form_rows:
            label = [class_name[len('field-'):] for class_name in form_row['class']
                     if class_name.startswith('field-')][0]
            # label = form_row.find('label')['for'][len('id_'):]

            field_tag = form_row.find('input')
            if not field_tag:
                field_tag = form_row.find('select')
            if not field_tag:
                field_tag = form_row.find('textarea')
            if not field_tag:
                field_tag = form_row.find('div', {'class': 'readonly'})
            if not field_tag:
                fields_dict[label] = '<N/A>'
                continue

            if field_tag.name == 'input':
                field_value = field_tag.get('value', '')
            elif field_tag.name == 'select':
                field_value = [option['value'] for option in field_tag.find_all(attrs={'selected': True})]
            elif field_tag.name in ['textarea', 'div']:
                field_value = field_tag.string.strip()
            else:
                field_value = None
            fields_dict[label] = field_value

        return {'_response': resp, 'details': fields_dict}

    def delete(self, object_id):
        path = self._path.rstrip('/')

        path = '{path}/{object_id}/delete/'.format(path=path, object_id=object_id)
        resp = self._da.post_with_csrf_and_auto_login(path, data={'post': 'yes'})
        return {'_response': resp['response'], 'success': resp['errors'] == []}


class DjangoAdminWithModels:
    def __init__(self, base_url=None, superuser_email=None, superuser_password=None, client=None, session=None):
        if client:
            self._django_admin = client
        else:
            self._django_admin = DjangoAdminBase(
                base_url=base_url,
                superuser_email=superuser_email,
                superuser_password=superuser_password,
                session=session
            )

    def _create_model(self, path: str, fields: dict = None):
        return DjangoAdminModel(
            django_admin=self._django_admin,
            path=path,
            fields=fields
        )


class DjangoAdminDynamic(DjangoAdminWithModels):
    def __init__(self, spec: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._spec = spec

    @classmethod
    def from_spec(cls, spec: dict, base_url=None, superuser_email=None, superuser_password=None, client=None, session=None):
        da = cls(
            base_url=base_url,
            superuser_email=superuser_email,
            superuser_password=superuser_password,
            spec=spec,
            client=client
        )
        for model_name, model_spec in spec["models"].items():
            model = da._create_model(path="/{app}/{name}/".format(**model_spec), fields=model_spec['fields'])
            setattr(da, model_name, model)

        return da
