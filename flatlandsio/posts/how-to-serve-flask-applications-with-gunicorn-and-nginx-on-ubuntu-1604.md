### Introduction

This guide is originally from [Digitalocean](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-16-04). Full credit goes to them, this is just a condensed version for my reference.

### Install the Components from the Ubuntu Repositories

Update your local package index and then install the packages.

Python 3, type:

```
$ sudo apt-get update
$ sudo apt-get install python3-pip python3-dev nginx
```

#### Create the WSGI Entry Point

Create a file that will serve as the entry point for our application.

```
$ nano ~/myproject/wsgi.py
```

We import the Flask instance from our app and then run it:

> ~/myproject/wsgi.py

```
from myproject import app


if __name__ == "__main__":
    app.run()
```

#### Testing Gunicorn's Ability to Serve the Project

```
$ cd ~/myproject
$ gunicorn --bind 0.0.0.0:5000 wsgi:app
```

### Create a systemd Unit File

Creating a systemd unit file will allow Ubuntu's init system to automatically start Gunicorn and serve our Flask application whenever the server boots.

Create a unit file ending in .service within the /etc/systemd/system directory to begin:

```
$ sudo nano /etc/systemd/system/myproject.service
```

> /etc/systemd/system/myproject.service

```
[Unit]
Description=Gunicorn instance to serve myproject
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/home/sammy/myproject
Environment="PATH=/home/sammy/myproject/myprojectenv/bin"
ExecStart=/home/sammy/myproject/myprojectenv/bin/gunicorn --workers 3 --bind unix:myproject.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```

Start and enable Gunicorn service:

```
$ sudo systemctl start myproject
$ sudo systemctl enable myproject
```

To ensure gunicorn is set up correctly there should be a myproject.sock file inside the project.

### Configuring Nginx to Proxy Requests

Begin by creating a new server block configuration file in Nginx's sites-available directory. We'll simply call this myproject to keep in line with the rest of the guide:

```
$ sudo nano /etc/nginx/sites-available/myproject
```

> /etc/nginx/sites-available/myproject

```
server {
    listen 80;
    server_name server_domain_or_IP;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/sammy/myproject/myproject.sock;
    }
}
```

Link the file to the sites-enabled directory:

```
$ sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
```

Test for syntax errors:

```
$ sudo nginx -t
```

Restart the Nginx process:

```
$ sudo systemctl restart nginx
```