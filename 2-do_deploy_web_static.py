#!/usr/bin/python3
"""
A fabfile to prepare the static file for deploying
"""
from fabric.api import *
from datetime import datetime
import os
import os.path


env.hosts = ['18.207.207.212', '54.237.74.142']


def do_pack():
    """
    function which generates a .tgz archive from the contents
    of web-static in order to prepare it to be pushed to the
    server
    """
    date = datetime.now()
    name = date.strftime('%Y%m%d%H%M%S')

    if not os.path.isdir('versions'):
        os.mkdir('versions')

    try:
        result = local("tar -cvzf versions/web_static_{}.tgz web_static".format(name))

        size = os.path.getsize("versions/web_static_{}.tgz".format(name))
        return "versions/web_static_{}.tgz".format(name)
    except Exception:
        return False


def do_deploy(archive_path):
    """
    push and uncompress the archive file in the `archive_path` to the server/s
    """
    if archive_path is None or not os.path.isfile(archive_path):
        return False
    try:
        result = put(local_path=archive_path, remote_path='/tmp/')
        name = os.path.basename(archive_path).split('.')[0]

        result = run("mkdir -p /data/web_static/releases/{}/".format(name))
        result = run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/".format(name, name))
        result = run("cp -rf /data/web_static/releases/{}/web_static/* ".format(name) +
                     "/data/web_static/releases/{}/".format(name))
        result = run("rm -rf /data/web_static/releases/{}/web_static".format(name))
        result = run("rm -rf /tmp/{}.tgz".format(name))
        result = run("rm -rf /data/web_static/current")
        result = run("ln -s /data/web_static/releases/{}/ ".format(name) +
                     "/data/web_static/current")
        print("New version deployed!")
        return True
    except Exception:
        return False
