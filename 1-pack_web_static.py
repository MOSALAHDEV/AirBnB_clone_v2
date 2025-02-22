#!usr/bin/python3
"""This module is a package of the web_static folder"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """This function packs the web_static folder"""
    try:
        local("mkdir -p versions")
        time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        local(f"tar -cvzf versions/web_static_{time_stamp}.tgz web_static")
        return f"versions/web_static_{time_stamp}.tgz"
    except:
        return None
