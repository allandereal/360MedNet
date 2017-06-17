from MedNet.settings import prod, dev
from fabric.context_managers import settings, cd
from fabric.operations import run, sudo


def deploy(dest='dev', user='faith', git_hash=None, syncdb=False, restart_celery=False,
           source='https://github.com/faithNassiwa/360MedNet.git'):
    if dest == 'prod':
        print("Deploying to prod")
        proc_name = '360MedNet'
        path = '/var/www/prod/360MedNet/'
        workon = ' /home/faith/.virtualenvs/prod_360MedNet/bin/'
        port = prod.SERVER_PORT
        pip = 'requirements.txt'
    else:
        print("Deploying to dev")
        proc_name = '360MedNet'
        path = '/var/www/dev/360MedNet/'
        workon = ' /home/faith/.virtualenvs/dev_360MedNet/bin/'
        port = dev.SERVER_PORT
        pip = 'requirements.txt'

    with settings(warn_only=True):
        if run("test -d %s" % path).failed:
            run("git clone %s %s" % (source, path))
            with cd(path):
                run("git config core.filemode false")
    with cd(path):
        run("git stash")
        if not git_hash:
            run("git pull origin master")
        else:
            run("git fetch")
            run("git checkout %s" % git_hash)
        run("%spip install -r %s" % (workon, pip))

        if syncdb:
            run("%spython manage.py migrate" % workon)
        sudo("chown -R %s:%s ." % (user, user))
        sudo("chmod -R ug+rwx .")
        run("export DJANGO_SETTINGS='settings/%s.py' && %snosetests" % (dest, workon))
    sudo("supervisorctl stop %s" % proc_name)
    with settings(warn_only=True):
        output = run("sudo fuser %d/tcp" % port)
        if output:
            proc_id = output.split()[1].strip()
            sudo("kill -9 %s" % proc_id)
    sudo("supervisorctl start %s" % proc_name)
    if dest == 'prod' and restart_celery:
        sudo("supervisorctl restart webhooks_celery")