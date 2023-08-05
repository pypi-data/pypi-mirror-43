# Django Admin client

## Installation

```
pip install django-admin-client
```

## Usage

3 main usages:
1. Convenient HTTP GET and POST methods
2. Dynamic Django Admin python client
3. Generating specific Django Admin python client

### 1. Convenient HTTP GET and POST methods

`DjangoAdminBase` will do auto login, session management, and auto csrf token inclusion and auto error detection

```python
from django_admin_client import DjangoAdminBase

basic_client = DjangoAdminBase('http://127.0.0.1:9000/admin', 'superuser', 'why-dont-tell-mom?')

# auto login:
basic_client.get_with_auto_login('/')
# <Response [200]>

# response is just our favorite and well-known response from 'requests' library
type(basic_client.get_with_auto_login('/'))
# requests.models.Response

# auto login (if not yet logged in or session expired),
# csrf token included in POST request automatically,
# errors in response html form detected and provided
basic_client.post_with_csrf_and_auto_login(
    '/auth/user/add/',
    {'username': 'test', 'password1': '123', 'password2': '123'}
)
#{'response': <Response [200]>,
# 'errors': [<div class="form-row errors field-password2">
#  <ul class="errorlist"><li>This password is too short. It must contain at least 8 characters.</li><li>This password is too common.</li><li>This password is entirely numeric.</li></ul>
#  <div>
#  <label class="required" for="id_password2">Password confirmation:</label>
#  <input id="id_password2" name="password2" required="" type="password"/>
#  <div class="help">Enter the same password as before, for verification.</div>
#  </div>
#  </div>]}

basic_client.post_with_csrf_and_auto_login(
    '/auth/user/add/',
    {'username': 'test', 'password1': 'isthislongenough', 'password2': 'isthislongenough'}
)
# {'response': <Response [200]>, 'errors': []}
```

### 2. Dynamic Django Admin python client

`DjangoAdminBase` can also do introspection on Django Admin site and generate specification.

```python
In [1]: spec = basic_client.generate_spec()
In [2]: import json
In [3]: json.dumps(spec, indent=2)
Out[3]:
{
  "models": {
    "groups": {
      "id": "groups",
      "app": "auth",
      "name": "group",
      "fields": {
        "name": {
          "name": "name",
          "required": true,
          "default_value": ""
        },
        "permissions": {
          "name": "permissions",
          "required": false,
          "default_value": ""
        }
      }
    },
    "users": {
      "id": "users",
      "app": "auth",
      "name": "user",
      "fields": {
        "username": {
          "name": "username",
          "required": true,
          "default_value": ""
        },
        "password1": {
          "name": "password1",
          "required": true,
          "default_value": ""
        },
        "password2": {
          "name": "password2",
          "required": true,
          "default_value": ""
        }
      }
    }
  }
}
```

This specification can then be fed to `DjangoAdminDynamic` class to get dynamic admin python client.

```python
from django_admin_client import DjangoAdminBase, DjangoAdminDynamic
basic_client = DjangoAdminBase('http://127.0.0.1:9000/admin', 'superuser', 'why-dont-tell-mom?')
spec = basic_client.generate_spec()
dynamic_client = DjangoAdminDynamic(spec=spec, client=basic_client)
dynamic_client.users.all()
# {'response': <Response [200]>, 'ids': ['1', '2']}
```

At the moment you can add objects with `<model-name>.add(item: dict)`:
```python
dynamic_client.users.add({})
#{'id': None,
# 'created': False,
# 'errors': [<div class="form-row errors field-username">
#  <ul class="errorlist"><li>This field is required.</li></ul>
#  <div>
#  <label class="required" for="id_username">Username:</label>
#  <input autofocus="" class="vTextField" id="id_username" maxlength="150" name="username" required="" type="text"/>
#  <div class="help">Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</div>
#  </div>
#  </div>, <div class="form-row errors field-password1">
#  <ul class="errorlist"><li>This field is required.</li></ul>
#  <div>
#  <label class="required" for="id_password1">Password:</label>
#  <input id="id_password1" name="password1" required="" type="password"/>
#  <div class="help"><ul><li>Your password can't be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can't be a commonly used password.</li><li>Your password can't be entirely numeric.</li></ul></div>
#  </div>
#  </div>, <div class="form-row errors field-password2">
#  <ul class="errorlist"><li>This field is required.</li></ul>
#  <div>
#  <label class="required" for="id_password2">Password confirmation:</label>
#  <input id="id_password2" name="password2" required="" type="password"/>
#  <div class="help">Enter the same password as before, for verification.</div>
#  </div>
#  </div>],
# 'response': <Response [200]>}

dynamic_client.users.add({'username': 'fromdynamic', 'password1': 'qwertyuio!', 'password2': 'qwertyuio!'})
# {'id': '3', 'created': True, 'errors': [], 'response': <Response [200]>}
```

Get all object ids with `<model-name>.all()`:
```python
dynamic_client.users.all()
# {'ids': ['3', '1', '2'], 'response': <Response [200]>}
```

Search object id with `<model-name>.find(query: str)`:
```python
dynamic_client.users.find('fromdynamic')
# {'id': '3', 'response': <Response [200]>}
```

Get object fields with `<model-name>.get(object_id: str)`:
```python
>>> dynamic_client.users.get('3')
{'response': <Response [200]>,
 'details': {'username': 'fromdynamic',
  'password': '<N/A>',
  'first_name': '',
  'last_name': '',
  'email': '',
  'is_active': '',
  'is_staff': '',
  'is_superuser': '',
  'groups': [],
  'user_permissions': [],
  'last_login_0': '',
  'last_login_1': '',
  'date_joined_0': '2019-03-06',
  'date_joined_1': '13:00:00'}}
```

Change object with `<model-name>.change(object_id: str, fields: dict)`:
```python
In [1]: dynamic_client.users.change('3', {'is_superuser': '1'})
Out[1]:
{'success': False, 'errors': [<div class="form-row errors field-username">
  <ul class="errorlist"><li>This field is required.</li></ul>
  <div>
  <label class="required" for="id_username">Username:</label>
  <input class="vTextField" id="id_username" maxlength="150" name="username" required="" type="text"/>
  <div class="help">Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</div>
  </div>
  </div>, <div class="form-row errors field-date_joined">
  <ul class="errorlist"><li>This field is required.</li></ul>
  <div>
  <label class="required" for="id_date_joined_0">Date joined:</label>
  <p class="datetime">
    Date: <input class="vDateField" id="id_date_joined_0" name="date_joined_0" required="" size="10" type="text"/>
  <br/>
    Time: <input class="vTimeField" id="id_date_joined_1" name="date_joined_1" required="" size="8" type="text"/>
  </p><input id="initial-id_date_joined_0" name="initial-date_joined_0" type="hidden"/>
  <input id="initial-id_date_joined_1" name="initial-date_joined_1" type="hidden"/>
  </div>
  </div>], 'response': <Response [200]>}

In [2]: dynamic_client.users.change('3',
   ...: {'username': 'fromdynamic',
   ...:   'is_active': '1',
   ...:   'is_staff': '1',
   ...:   'is_superuser': '1',
   ...:   'date_joined_0': '2019-03-06', 'date_joined_1': '13:00'})
Out[2]: {'success': True, 'errors': [], 'response': <Response [200]>}

In [3]: dynamic_client.users.get('3')
Out[3]:
{'response': <Response [200]>,
 'details': {'username': 'fromdynamic',
  'password': '<N/A>',
  'first_name': '',
  'last_name': '',
  'email': '',
  'is_active': '1',
  'is_staff': '1',
  'is_superuser': '1',
  'groups': [],
  'user_permissions': [],
  'last_login_0': '',
  'last_login_1': '',
  'date_joined_0': '2019-03-06',
  'date_joined_1': '13:00:00'}}



```

And delete the object with `<model-name>.delete(object_id: str)`:
```python
dynamic_client.users.delete('3')
# {'response': <Response [200]>, 'success': True}

dynamic_client.users.all()
# {'response': <Response [200]>, 'ids': ['1', '2']}
```

### 3. Generating specific Django Admin python client

`DjangoAdminDynamic` is quite useful for quick terminal sessions.

Auto-completion for `DjangoAdminDynamic` clients is provided in python interpreter when hitting `<tab>` because attributes
of a client are introspected at run time with `dir` built-in python funciton.

But writing source code with `DjangoAdminDynamic` is not that pleasant because
there's no way for IDE to know what attributes will object have at run time.

For this purpose `generate-package` command is provided with `django-admin-package`.

Example
```
$ generate-package
Base url (including /admin): http://localhost:9000/admin
Superuser username: superuser
Superuser password:
Site name: fresh project
Path to package (default: /tmp): .
Version (default: 1.0):
Generated package in ./freshproject-admin-client
```

Generated project structure:
```
$ tree freshproject-admin-client
freshproject-admin-client
├── freshproject_admin_client
│   ├── client.py
│   ├── __init__.py
│   └── spec.json
├── README.md
└── setup.py

1 directory, 5 files
```

You can version control generated package, install it, upload to PyPI.

Example usage of a generated client:
```
$ ipython
Python 3.6.7 (default, Nov  9 2018, 21:20:52)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.3.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from freshproject_admin_client import FreshProjectDjangoAdminClient

In [2]: client = FreshProjectDjangoAdminClient('http://localhost:9000/admin', 'superuser', 'why-dont-tell-mom?')

In [3]: client.auth.users.all()
Out[3]: {'response': <Response [200]>, 'ids': ['4', '1', '2']}

In [4]: client.auth.users.add()
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-4-213c8509773c> in <module>
----> 1 client.auth.users.add()

TypeError: add() missing 3 required positional arguments: 'username', 'password1', and 'password2'

In [5]: client.auth.users.add('from_freshproject_client', '123qweASD)_+', '123qweASD)_+')
Out[5]: {'response': <Response [200]>, 'id': '5', 'created': True}

In [6]: client.auth.users.get('5')
Out[6]:
{'response': <Response [200]>,
 'details': {'username': 'from_freshproject_client',
  'password': '<N/A>',
  'first_name': '',
  'last_name': '',
  'email': '',
  'is_active': '',
  'is_staff': '',
  'is_superuser': '',
  'groups': [],
  'user_permissions': [],
  'last_login': '',
  'date_joined': '2019-03-05'}}

In [7]: client.auth.users.find('from_freshproject_client')
Out[7]: {'response': <Response [200]>, 'id': '5'}

In [8]: client.auth.users.delete('5')
Out[8]: {'response': <Response [200]>, 'success': True}
```