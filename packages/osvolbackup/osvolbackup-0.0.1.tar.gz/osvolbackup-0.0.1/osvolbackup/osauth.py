import os
from keystoneauth1 import loading
from keystoneauth1 import session

VERSION = 2
USERNAME = os.environ.get('OS_USERNAME')
AUTH_URL = os.environ.get('OS_AUTH_URL')
PASSWORD = os.environ.get('OS_PASSWORD')
PROJECT_NAME = os.environ.get('OS_PROJECT_NAME')
USER_DOMAIN_NAME = os.environ.get('OS_USER_DOMAIN_NAME')
PROJECT_DOMAIN_NAME = os.environ.get('OS_PROJECT_DOMAIN_NAME')


def get_session():
    loader = loading.get_plugin_loader('password')
    auth = loader.load_from_options(
            auth_url=AUTH_URL, username=USERNAME, password=PASSWORD,
            project_name=PROJECT_NAME, project_domain_name=PROJECT_DOMAIN_NAME,
            user_domain_name=USER_DOMAIN_NAME

        )
    return session.Session(auth=auth)
