from fabric.api import run, env, cd, sudo, prefix


def testing():
    env.host_string = "linkfloyd.com"
    env.user = "miratcan"
    env.webapp = "/home/miratcan/webapps/linkfloyd/linkfloyd/linkfloyd/"
    env.activate_env = 'source /home/miratcan/envs/linkfloyd/bin/activate'

def _virtualenv(command):
    with cd(env.directory):
        sudo(env.activate + '&&' + command)

def pull():
    run('git pull')

def update_libs():
    run('pip install -r ../requirements.txt')

def syncdb():
    run('python manage.py syncdb --noinput --migrate')

def restart_server():
    run('../../apache2/bin/restart')

def collect_static():
    run('python manage.py collectstatic --noinput')

def update_scores():
    run('python manage.py update_scores')
 

def deploy():
    with prefix(env.activate_env):
        with cd(env.webapp):
           pull()
           update_libs()
           syncdb()
           collect_static()
           restart_server()

