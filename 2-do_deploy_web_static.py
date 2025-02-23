#!/usr/bin/python3
""" Fabric script that distributes an archive to web servers """
from fabric.api import env, local, run, put
import os


env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'
env.hosts = ['100.26.168.254', '44.211.253.220']

def do_deploy(archive_path):
    """ Distributes an archive to web servers """
    if not os.path.exists(archive_path):
        return False
    try:
        filename = os.path.basename(archive_path)
        without_ex = filename.split('.')[0]
        release_path = f'/data/web_static/releases/{without_ex}'
        put(archive_path, '/tmp/')
        run(f'mkdir -p {release_path}')
        run(f'tar -xzf /tmp/{filename} -C {release_path}')
        run(f'rm /tmp/{filename}')
        run(f'mv {release_path}/web_static/* {release_path}/')
        run(f'rm -rf {release_path}/web_static')
        run('rm -rf /data/web_static/current')
        run(f'ln -s {release_path}/ /data/web_static/current')
        return True
    except:
        return False
