from fabric.api import run, env, cd, sudo, prefix


def testing():
    env.host_string = "linkfloyd.com"
    env.user = "miratcan"
    env.password = "kurukasap"
    env.webapp = "/home/miratcan/webapps/linkfloyd/linkfloyd/linkfloyd/"

    env.activate_env = 'source /home/miratcan/envs/linkfloyd/bin/activate'

def _virtualenv(command):
    with cd(env.directory):
        sudo(env.activate + '&&' + command)

def pull():
    with cd(env.webapp):
        run('git pull')

def update_libs():
    with prefix(env.activate_env):
        with cd(env.webapp):
            run('pip install -r ../requirements.txt')
            run('python manage.py collectstatic --noinput')
            run('python manage.py syncdb --noinput')
            run('../../apache2/bin/restart')

def deploy():
    pull()
    update_libs()



