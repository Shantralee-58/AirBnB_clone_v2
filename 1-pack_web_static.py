#!/usr/bin/python3
from fabric import task
from datetime import datetime

@task
def do_pack(c):
    """Packs the web static files into a .tgz archive."""
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_file = f"versions/web_static_{current_time}.tgz"
    c.local("mkdir -p versions")
    c.local("tar -czvf {} web_static".format(archive_file))
    return archive_file
