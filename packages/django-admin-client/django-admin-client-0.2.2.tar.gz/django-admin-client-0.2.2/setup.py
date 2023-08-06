from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='django-admin-client',
    version='0.2.2',
    description='Django admin client',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/y3g0r/django-admin-client',
    author='Yegor Ivashchenko',
    author_email='yegor.ivashchenko@protonmail.com',
    license='MIT',
    packages=['django_admin_client'],
    install_requires=[
        'requests',
        'BeautifulSoup4',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'generate-spec=django_admin_client.command_line.generate_spec:main',
            'generate-package=django_admin_client.command_line.generate_package:main',
        ]
    },
    zip_safe=False
)
