### Introduction

This guide is originally from [Miguel Grinberg](https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https) and [Digitalocean](http://https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-16-04). Full credit goes to them, this is just a condensed version for my reference.

### Using Let's Encrypt for free SSL Certs

Getting a certificate from Let's Encrypt is fairly easy, begin by installing their open source certbot tool on your server:

```
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository ppa:certbot/certbot
$ sudo apt-get update
$ sudo apt-get install certbot
```

we'll be using the nginx plugin:

```
sudo apt-get install python-certbot-nginx
```

### Obtaining an SSL Certificate

```
$ sudo certbot --nginx -d example.com -d www.example.com
```

If certbot is able to verify the domain, it will write the certificate file as /etc/letsencrypt/live/example.com/fullchain.pem and the private key as /etc/letsencrypt/live/example.com/privkey.pem, and these are going to be valid for a period of 90 days.

If you are using nginx as reverse proxy, you can take advantage of the powerful mappings. In the following example, I extended the HTTP server block shown in the previous section to send all Let's Encrypt related requests to a specific directory of your choice:

```
server {
    listen 80;
    server_name example.com www.exmaple.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/deploy/example_app/exmaple_app/example.sock;
        return 301 https://$host$request_uri;
    }
}
```

Finally add the ssl certs to a new nginx server block

```
server {
    listen 443 ssl;
    server_name example.com www.example.com;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/deploy/example_app/exmaple_app/example.sock;
```



Certbot is also used when you need to renew the certificates, which will expire every 90 days. Issue the following command:

```
$ sudo certbot renew
```

### Additional Steps: Achieving an SSL A+ Grade

One of the areas in which it is easy to make an improvement is in how the coefficients that are used during the encryption key exchange are generated. Using the openssl tool, you can run the following command:

```
$ openssl dhparam -out /path/to/dhparam.pem 2048
```

This command is going to take some time to run. when it's done, you will have a dhparam.pem file with strong coefficients that you can plug into the ssl server block in nginx:

```
$ ssl_dhparam /path/to/dhparam.pem;
```

Next, you will probably need to configure which ciphers the server allows for the encrypted communication.

```
server {
    listen 443 ssl;
    server_name example.com;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_dhparam /path/to/dhparam.pem;
    ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-DSS-AES128-GCM-SHA256:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-DSS-AES128-SHA256:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:DHE-RSA-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:AES:CAMELLIA:!DES-CBC3-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_stapling on;
    ssl_stapling_verify on;
    add_header Strict-Transport-Security max-age=15768000;
    # ...
}
```