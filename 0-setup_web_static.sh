#!/usr/bin/env bash
# Configure web-02 to be identical to web-01

sudo apt update -y
sudo apt install nginx -y
mkdir -p /var/www/html
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "Hello World!" | sudo tee /var/www/html/index.html > /dev/null
echo "Ceci n'est pas une page" | sudo tee /var/www/html/404.html > /dev/null
echo '
<html>
<head>
<title>ALX</title>
</head>
<body>
ALX School
</body>
</html>
' | sudo tee /data/web_static/releases/test/index.html > /dev/null

ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

sudo bash -c "cat > /etc/nginx/sites-available/default <<EOF
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    add_header X-Served-By $(hostname);

    root /var/www/html;
    index index.html;

    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html;
    }

    location /redirect_me {
        return 301 http://\$host/index.html;
    }

    error_page 404 /404.html;
    location = /404.html {
        root /var/www/html;
        internal;
    }
}
EOF"

# restart Nginx
sudo service nginx restart
