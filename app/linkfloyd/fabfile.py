from fabric.api import run, env, cd, local, sudo, prefix


def testing():
    env.host_string = "web77.webfaction.com"
    env.user = "miratcan"
    env.password = "kukuleta"
    env.webapp = "/home/miratcan/webapps/linkfloyd/linkfloyd/app/linkfloyd"

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
            run('pip install -r ../../docs/reqs.txt')
            run('python manage.py collectstatic --noinput')
            run('python manage.py syncdb --noinput')
            run('python manage.py migrate')
            run('../../../apache2/bin/restart')

def deploy():
    pull()
    update_libs()



