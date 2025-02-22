#!/usr/bin/python3
""" Fabric script that distributes an archive to web servers """
from fabric.api import env, local, run, put
import os.path


env.hosts = ['100.26.168.254']

def do_deploy(archive_path):
    """ Distributes an archive to web servers """
    if not os.path.exists(archive_path):
        return False
    try:
        filename = archive_path.split('/')[1]
        without_ex = filename.split('.')[0]
        path = '/data/web_static/releases/' + without_ex
        put(archive_path, '/tmp/')
        run('mkdir -p {}/'.format(path))
        run('tar -xzf /tmp/{} -C {}/'.format(filename, path))
        run('rm /tmp/{}'.format(filename))
        run('mv {}/web_static/* {}/'.format(path, path))
        run('rm -rf {}/web_static'.format(path))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(path))
        return True
    except:
        return False
