#!/usr/bin/env bash
# This script sets up the web servers for the deployment of web_static.

# Install Nginx if not already installed
sudo apt-get update
sudo apt-get -y install nginx

# Create necessary folders
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared
sudo touch /data/web_static/releases/test/index.html
echo "<html><head></head><body>Holberton School</body></html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link
sudo rm -rf /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Set ownership
sudo chown -R ubuntu:ubuntu /data/
sudo sed -i "/location \/hbnb_static {/ {n; s/alias.*/alias \/data\/web_static\/current\/;/}" /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart
