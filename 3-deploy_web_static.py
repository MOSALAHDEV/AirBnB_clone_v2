#!/usr/bin/python3
""" Fabric script that distributes an archive to web servers """
from fabric.api import local, env, run, put
import os
from datetime import datetime


env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'
env.hosts = ['100.26.168.254', '44.211.253.220']


def do_pack():
    """ Generates a .tgz archive from the contents of web_static """
    try:
        local('mkdir -p versions')
        date = datetime.now()
        filename = f'versions/web_static_{date.strftime("%Y%m%d%H%M%S")}.tgz'
        local(f'tar -cvzf {filename} web_static')
        return filename
    except:
        return None

def deploy():
    """ Distributes an archive to web servers """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

def do_deploy(archive_path):
    """ Distributes an archive to web servers """
    if not os.path.exists(archive_path):
        return False
    try:
        form = '%Y-%m-%dT%H:%M:%S.%f'
        filename = os.path.basename(archive_path)
        without_ex = filename.split('.')[0]
        date = datetime.strptime(without_ex, form)
        release_path = f'/data/web_static/releases/web_static_{date.strftime("%Y%m%d%H%M%S")}'
        put(archive_path, '/tmp/')
        run(f'mkdir -p {release_path}')
        run(f'tar -xzf /tmp/{filename} -C {release_path}')
        run(f'rm /tmp/{filename}')
        run(f'mv {release_path}/web_static/* {release_path}/')
        run(f'rm -rf {release_path}/web_static')
        run(f'rm -rf /data/web_static/current')
        run(f'ln -s {release_path}/ /data/web_static/current')
        return True
    except Exception as e:
        return False
