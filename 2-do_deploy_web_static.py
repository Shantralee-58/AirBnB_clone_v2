#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists

env.hosts = ['18.207.207.212', '54.237.74.142']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_name = archive_path.split("/")[-1]
        no_extension = file_name.split(".")[0]
        path = "/data/web_static/releases/"

        put(archive_path, '/tmp/')
        run('sudo mkdir -p {}{}/'.format(path, no_extension))
        run('sudo tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, no_extension))
        run('sudo rm /tmp/{}'.format(file_name))
        run('sudo mkdir -p /data/web_static/releases/{}/web_static/'.format(no_extension))
        run('sudo rsync -a --delete /data/web_static/releases/{}/web_static/ /data/web_static/releases/{}/'.format(no_extension, no_extension))
        run('sudo mkdir -p /data/web_static/releases/{}/web_static/'.format(no_extension))
        run('sudo rm -rf /data/web_static/releases/{}/web_static/*'.format(no_extension))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {}{}/ /data/web_static/current'.format(path, no_extension))

        print("New version deployed!")
        return True
    except Exception as e:
        print("Error: {}".format(e))
        return False
