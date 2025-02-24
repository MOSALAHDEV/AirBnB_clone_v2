#!/usr/bin/python3
""" Fabric script that distributes an archive to web servers """
from fabric.api import local, env, run, put
import os
from datetime import datetime


env.hosts = ['100.26.168.254', '44.211.253.220']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """ Generates a .tgz archive from the contents of web_static """
    try:
        time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{time_stamp}.tgz"
        local("mkdir -p versions")
        local(f"tar -cvzf {archive_path} web_static")
        return archive_path
    except Exception as e:
        return None


def do_deploy(archive_path):
    """ Distributes an archive to web servers """
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')
        filename = os.path.basename(archive_path)
        la = filename.split(".")[0]
        release_path = f'/data/web_static/releases/web_static_{la}'
        run(f'mkdir -p {release_path}')
        run(f'tar -xzf /tmp/{filename} -C {release_path}')
        run(f'rm /tmp/{filename}')
        local('mkdir -p versions')
        local(f'tar -cvzf {archive_path} web_static')
        run(f'mv {release_path}/web_static/* {release_path}/')
        run(f'rm -rf {release_path}/web_static')
        run(f'rm -rf /data/web_static/current')
        run(f'ln -s {release_path}/ /data/web_static/current')
        return True
    except Exception as e:
        return False


def deploy():
    """ Distributes an archive to web servers """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
