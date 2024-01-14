#!/usr/bin/env bash
# sets the web server for the deployment

## install nginx
apt-get update &> /dev/null
apt-get install -y nginx &> /dev/null

## create the required directories
mkdir -p /data/web_static/releases/test
mkdir -p /data/web_static/shared

## create a fake html file for test
echo -e "<!DOCTYPE html>
<html lang='en'>
\t<head>
\t\t<titel>Test</titel>
\t\t<meta charset='utf-8'>
\t</head>
\t<body>
\t\t<h1>Test Nginx Auto-setup</h1>
\t\t<p>Test the auto configuration for the web server and the deployment
\t\t   of the static contenct</p>
\t</body>
</html>" > /data/web_static/releases/test/index.html

## create a link of releases/test in current
ln -snf /data/web_static/releases/test /data/web_static/current

## change the owner/group of /data/ to user 'ubuntu'
chown -R ubuntu:ubuntu /data

## update nginx configuration to serve the contect of current/
## when requesting hbnb_static/

default_file="/etc/nginx/conf.d/default.conf"
touch "$default_file" # just in case

## over-write the default configuration file
echo -e "server {
    listen       80  default_server;
    server_name  18.214.87.146;
    root         /var/www/html;
    error_page   404        /404.html;
    add_header   X-Served-By  \$hostname always;

    location = / {
        index   /index.html;
    }

    location /redirect_me {
        return  301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
    }

    location /hbnb_static {
    	alias   /data/web_static/current/;
    }
}" > "$default_file"

sed -i 's/default_server;/;/g' /etc/nginx/sites-enabled/default

## relaod nginx server
service nginx start
nginx -s reload
exit 0