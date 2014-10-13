from fabric.api import run, cd

def install():
        run('unddame -s')
        sudo('apt-get update')
        sudo('apt-get install -y python-pip')
        sudo('pip install fig')
        run('git clone https://github.com/ska-sa/ceiling-kat')

def run():
        cd('ceiling-kat/surf_kat')
        sudo('fig up')
