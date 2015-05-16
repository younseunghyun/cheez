from fabric.api import (
    run,
    local,
    sudo,
    cd,
    lcd,
    env,
)
from fabric.contrib.files import exists
from local_config import *

env.hosts = HOSTS
env.user = USER


def prepare():
    sudo('apt-get update')
    sudo('apt-get install -y build-essential git')
    sudo('apt-get install -y python3')
    sudo('apt-get install -y nginx')
    sudo('apt-get install -y supervisor')
    sudo('apt-get install -y python3-pip')
    sudo('apt-get install -y python-virtualenv')
    sudo('apt-get install -y libmysqlclient-dev')
    sudo('pip3 install uwsgi')
    generate_openssl_cert()

def generate_openssl_cert():
    sudo('mkdir /etc/nginx/ssl')
    with cd('/etc/nginx/ssl'):
        sudo('openssl genrsa -des3 -out server.key 2048')
        sudo('openssl req -new -key server.key -out server.csr')
        sudo('cp server.key server.key.org')
        sudo('openssl rsa -in server.key.org -out server.key')
        sudo('openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt')
        sudo('service nginx restart')

def upload():
    with(lcd(LOCAL_PROJECT_DIR)):
        local('source venv/bin/activate')
        local('python cheez/manage.py collectstatic --noinput')
        local('pip freeze > requirements.txt')

    if not exists(REMOTE_PROJECT_DIR):
        run('mkdir -p {}'.format(REMOTE_PROJECT_DIR))

    for host in env.hosts:
        local('rsync -avz {1} ubuntu@{0}:{2}/../ --exclude "*.pyc" --exclude "venv" --exclude ".git" --exclude "fabfile.py" --exclude ".idea" --exclude "local_config.py" '.format(host, LOCAL_PROJECT_DIR, REMOTE_PROJECT_DIR))


def start():
    sudo('supervisorctl start {}'.format(PROJECT_NAME))


def stop():
    sudo('supervisorctl stop {}'.format(PROJECT_NAME))


def restart():
    sudo('supervisorctl restart {}'.format(PROJECT_NAME))


def migrate():
    with(lcd(LOCAL_PROJECT_DIR)):
        local('python cheez/manage.py makemigrations')
        local('python cheez/manage.py migrate')


def config():
    with(cd(REMOTE_PROJECT_DIR)):
        if not exists(REMOTE_PROJECT_DIR + '/venv'):
            run('virtualenv -p python3 venv')

        run('{}/venv/bin/pip install -r requirements.txt'.format(REMOTE_PROJECT_DIR))
        sudo('cp config/nginx/default /etc/nginx/sites-available/default')
        sudo('chown www-data:www-data {}/app.sock'.format(REMOTE_PROJECT_DIR))
        sudo('service nginx restart')

        sudo('cp config/supervisor/supervisor-app.conf /etc/supervisor/conf.d/supervisor-app.conf')
        sudo('supervisorctl reread')
        sudo('supervisorctl update')

def deploy():
    upload()
    config()
    restart()