#!/usr/bin/python3
"""
Fabric the script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists, basename
import os

env.hosts = ['18.207.207.212', '54.237.74.142']


def do_deploy(archive_path):
    """distributes archive to the web servers"""
    if not exists(archive_path):
        return False

    try:
        file_name = basename(archive_path)
        no_ext = os.path.splitext(file_name)[0]
        path = "/data/web_static/releases/"

        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, no_ext))

        if run('rm /tmp/{}'.format(file_name)).failed:
            return False

        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')

        if run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext)).failed:
            return False

        return True
    except Exception as e:
        print(e)
        return False
