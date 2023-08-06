from django_admin_client.helpers import SettingsFunctionality, NotSet


class Settings(SettingsFunctionality):
    ADMIN_BASE_URL = NotSet

    SUPERUSER_EMAIL = NotSet

    SUPERUSER_PASSWORD = NotSet

    SITE_NAME = NotSet

    PATH_TO_PACKAGE = '/tmp'

    PACKAGE_VERSION = '1.0'


settings = Settings()
