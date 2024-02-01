#!/usr/bin/python3
from fabric import task
from os import path

env.hosts = ['3.85.148.96', '54.234.58.58']
env.user = 'ubuntu'  # Replace with your SSH username

@task
def do_deploy(c, archive_path):
    """Distributes an archive to web servers"""
    if not path.exists(archive_path):
        return False

    filename = path.basename(archive_path)
    root = '/data/web_static/releases/'
    dest = f'{root}{filename.split(".")[0]}'

    # Upload the archive to the /tmp/ directory of the web server
    c.put(archive_path, '/tmp/')

    # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension>
    c.run(f'mkdir -p {dest}')
    c.run(f'tar -xzf /tmp/{filename} -C {dest}')

    # Delete the archive from the web server
    c.run(f'rm /tmp/{filename}')

    # Delete the symbolic link /data/web_static/current from the web server
    c.run('rm -rf /data/web_static/current')

    # Create a new symbolic link /data/web_static/current linked to the new version of your code
    c.run(f'ln -s {dest} /data/web_static/current')

    return True
