"""Deployment scripts using fabric."""
from fabric.api import cd, env, run, sudo
from fabric.contrib.project import rsync_project

app_dir = "/apps/loyalty/"
local_dir = "/home/iris/VMs/duka-vm-3/project/"
git_repo = "git@bitbucket.org:dukaconnect/loyalty.git"
env.use_ssh_config = True
user_dev = "vagrant"
user_live = "focus"


def local():
    """Local loyalty project host."""
    env.hosts = ["loyaltydev"]


def production():
    """Production loyalty project host."""
    env.hosts = ["duka"]


def sync():
    """Sync local files with development host."""
    rsync_project(
        "{}project".format(app_dir),
        local_dir=local_dir,
        exclude=["*.pyc", ".git*"]
    )
    with cd("{}project".format(app_dir)):
        manage_app()
    restart_app()
    return


def manage_app():
    """Do Django management."""
    sudo("/opt/venvs/loyalty/bin/pip install -r requirements.txt")
    run("/opt/venvs/loyalty/bin/python manage.py makemigrations")
    run("/opt/venvs/loyalty/bin/python manage.py migrate")
    run((
        "/opt/venvs/loyalty/bin/python manage.py"
        " collectstatic --noinput --clear"
    ))
    run("/opt/venvs/loyalty/bin/python manage.py test --noinput")


def restart_app():
    """Restart the app."""
    sudo('systemctl restart loyalty nginx')
