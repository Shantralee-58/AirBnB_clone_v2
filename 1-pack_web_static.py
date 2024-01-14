#!/usr/bin/python3
"""
A fabfile to prepare the static file for deploying
"""
from fabric.api import *
from datetime import datetime
import os
import os.path


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

    result = local(f"tar -cvzf versions/web_static_{name}.tgz web_static")

    if result.failed:
        return None

    size = os.path.getsize(f"versions/web_static_{name}.tgz")
    print(f"web_static packed: versions/web_static_{name}.tgz -> {size}Bytes")

    return f"versions/web_static_{name}.tgz"
