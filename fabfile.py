"""
Starter fabfile for deploying the PROJECTNAME project.

Change all the things marked CHANGEME. Other things can be left at their
defaults if you are happy with the default layout.
"""

import posixpath
import os
from fabric.api import run, local, env, settings, cd, task
from fabric.contrib.files import exists
from fabric.operations import _prefix_commands, _prefix_env_vars
#from fabric.decorators import runs_once
#from fabric.context_managers import cd, lcd, settings, hide

# CHANGEME
env.hosts = ['user@PROJECTNAME.example.com']
env.code_dir = '/srv/www/PROJECTNAME'
env.project_dir = '/srv/www/PROJECTNAME/PROJECTNAME'
env.static_root = '/srv/www/PROJECTNAME/static/'
env.virtualenv = '/srv/www/PROJECTNAME/.virtualenv'
env.code_repo = 'git@github.com:user/PROJECTNAME.git'

# Python version
PYTHON_BIN = "python"
PYTHON_PREFIX = ""  # e.g. /usr/local  Use "" for automatic
PYTHON_FULL_PATH = "%s/bin/%s" % (PYTHON_PREFIX, PYTHON_BIN) if PYTHON_PREFIX else PYTHON_BIN

# Javascript directory
JAVASCRIPT_DIR = os.path.join('project', 'static', 'js')
# Coffeescript directory
COFFEE_DIR = os.path.join('project', 'static', 'coffee')


def virtualenv(venv_dir):
    """
    Context manager that establishes a virtualenv to use.
    """
    return settings(venv=venv_dir)


def run_venv(command, **kwargs):
    """
    Runs a command in a virtualenv (which has been specified using
    the virtualenv context manager
    """
    run("source %s/bin/activate" % env.virtualenv + " && " + command, **kwargs)


def install_dependencies():
    ensure_virtualenv()
    with virtualenv(env.virtualenv):
        with cd(env.code_dir):
            run_venv("pip install -r requirements/prod.txt")


def ensure_virtualenv():
    if exists(env.virtualenv):
        return

    with cd(env.code_dir):
        run("virtualenv --no-site-packages --python=%s %s" %
            (PYTHON_BIN, env.virtualenv))
        run("echo %s > %s/lib/%s/site-packages/projectsource.pth" %
            (env.project_dir, env.virtualenv, PYTHON_BIN))


def ensure_src_dir():
    if not exists(env.code_dir):
        run("mkdir -p %s" % env.code_dir)
    with cd(env.code_dir):
        if not exists(posixpath.join(env.code_dir, '.git')):
            run('git clone %s .' % (env.code_repo))


def push_sources():
    """
    Push source code to server
    """
    ensure_src_dir()
    local('git push origin master')
    with cd(env.code_dir):
        run('git pull origin master')


@task
def version():
    """ Show last commit to the deployed repo. """
    with cd(env.code_dir):
        run('git log -1')


@task
def uname():
    """ Prints information about the host. """
    run("uname -a")


@task
def webserver_stop():
    """
    Stop the webserver that is running the Django instance
    """
    run("service apache2 stop")


@task
def webserver_start():
    """
    Starts the webserver that is running the Django instance
    """
    run("service apache2 start")


@task
def webserver_restart():
    """
    Restarts the webserver that is running the Django instance
    """
    if DJANGO_SERVER_RESTART:
        with cd(env.code_dir):
            run("touch %s/wsgi.py" % env.project_dir)
    else:
        with settings(warn_only=True):
            webserver_stop()
        webserver_start()


def restart():
    """ Restart the wsgi process """
    with cd(env.code_dir):
        run("touch %s/PROJECTNAME/wsgi.py" % env.code_dir)



@task
def first_deployment_mode():
    """
    Use before first deployment to switch on fake south migrations.
    """
    env.initial_deploy = True


@task
def sshagent_run(cmd):
    """
    Helper function.
    Runs a command with SSH agent forwarding enabled.

    Note:: Fabric (and paramiko) can't forward your SSH agent.
    This helper uses your system's ssh to do so.
    """
    # Handle context manager modifications
    wrapped_cmd = _prefix_commands(_prefix_env_vars(cmd), 'remote')
    try:
        host, port = env.host_string.split(':')
        return local(
            "ssh -p %s -A %s@%s '%s'" % (port, env.user, host, wrapped_cmd)
        )
    except ValueError:
        return local(
            "ssh -A %s@%s '%s'" % (env.user, env.host_string, wrapped_cmd)
        )

@task
def deploy():
    """
    Deploy the project.
    """
    with settings(warn_only=True):
        webserver_stop()
    push_sources()
    install_dependencies()
    webserver_start()

@task
def coffee(watch=1):
    '''
    Compiles Coffeescript files.

    Enters watch mode by default when you run:
        >> fab coffee
    To do a one-time compile, run:
        >> fab coffee:watch=0
    '''

    base_command = 'coffee -o {} '.format(JAVASCRIPT_DIR)
    coffee_files = "{}/*.coffee".format(COFFEE_DIR)
    if watch == 1:
        print "Watching .coffee files in {} to {}".format(COFFEE_DIR, JAVASCRIPT_DIR)
        command = base_command + '-cw ' + coffee_files
    else:
        print "Compiling .coffee files in {} and compiling them to {}".format(COFFEE_DIR, JAVASCRIPT_DIR)
        command = base_command + '-c ' + coffee_files
    local(command)

@task
def watchmedo():
    """
    Watches the file system for changes of ``*.py`` files and executes the tests
    whenever you save a file.
    """
    cmd = 'watchmedo shell-command --recursive --ignore-directories --patterns="*.py" --wait --command="fab test:unit=1,webtest=1" .'
    local(cmd)

@task
def test(unit=1, webtest=1):
    """
    Runs the tests.
    """
    command = 'nosetests --verbosity=2'
    if all == 0:
        if int(unit) == 0:
            command += " --exclude='unit_tests' "
        if int(webtest) == 0:
            command += " --exclude='webtest_tests' "
    local(command)
