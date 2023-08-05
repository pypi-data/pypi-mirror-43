init_py = """\
from .client import {name}DjangoAdminClient

"""

setup_py = """\
from setuptools import setup

setup(
    name='{project_name}',
    version='{package_version}',
    description='Python client for {name} django admin',
    license='MIT',
    packages=['{package}'],
    install_requires=[
        'django-admin-client'
    ],
    zip_safe=True,
)
"""

readme_md = """\
# {project_name}

"""