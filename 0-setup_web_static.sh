#!/usr/bin/env bash
# Set up a directory for the web static project
sudo apt-get update -y
sudo apt-get -y  install nginx
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
touch /data/web_static/releases/test/index.html
echo "Hello World!" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu:ubuntu /data/
sed -i '/listen 80 default_server/a location /hbnb_static/ {alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default
sudo service nginx restart
