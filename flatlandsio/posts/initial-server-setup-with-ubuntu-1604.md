### Introduction

This guide is originally from [Digitalocean](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-16-04). Full credit goes to them, this is just a condensed version for my reference.

### Step One — Root Login

If you are not already connected to your server, go ahead and log in as the root user using the following command (substitute the highlighted word with your server's public IP address):

```
$ ssh root@your_server_ip
```

There might be a warning about... [reproduce warning and document.]

### Step Two — Create a New User

While root enter the following and follow prompt:

```
$ adduser deploy
```

### Step Three — Root Privileges

Setting up a 'superuser' will allow our normal user to run commands with administrative privileges.

We do this by adding the new user to the 'sudo' group.

As root, run this command to add your new user to the sudo group:

```
$ usermod -aG sudo deploy
```

### Step Four — Add Public Key Authentication (Recommended)

##### Generate a Key Pair

If you do not already have an SSH key pair, which consists of a public and private key, you need to generate one. If you already have a key that you want to use, skip to the Copy the Public Key step.

To generate a new key pair, enter the following command at the terminal of your local machine:

```
$ ssh-keygen
```

This generates a private key, id_rsa, and a public key, id_rsa.pub, in the .ssh directory.

#### Copy the Public Key

##### Option 1: Use ssh-copy-id

If your local machine has the ssh-copy-id script installed, you can use it to install your public key to any user that you have login credentials for.

```
$ ssh-copy-id deploy@your_server_ip
```

##### Option 2: Manually Install the Key

Assuming you generated an SSH key pair using the previous step, use the following command at the terminal of your local machine to print your public key (id_rsa.pub):

```
$ cat ~/.ssh/id_rsa.pub
```

Select the public key, and copy it to your clipboard.

On the server, as the root user, enter the following command to temporarily switch to the new user:

```
$ su - deploy
```

Create a new directory called .ssh and restrict its permissions with the following commands:

```
$ mkdir ~/.ssh
$ chmod 700 ~/.ssh
```

```
$ nano ~/.ssh/authorized_keys
```

Now restrict the permissions of the authorized_keys file with this command:

```
$ chmod 600 ~/.ssh/authorized_keys
```

### Step Five — Disable Password Authentication (Recommended)

Only disable password authentication if you installed a public key to your user.

As root or your new sudo user, open the SSH daemon configuration:

```
$ sudo nano /etc/ssh/sshd_config
```

Find the line that specifies PasswordAuthentication, uncomment it by deleting the preceding #, then change its value to "no". It should look like this after you have made the change:

```
PasswordAuthentication no
```

Here are two other settings that are important for key-only authentication and are set by default. If you haven't modified this file before, you do not need to change these settings:

```
PubkeyAuthentication yes
ChallengeResponseAuthentication no
```

Finally reload the SSH daemon:

```
$ sudo systemctl reload sshd
```

### Step Six — Test Log In

```
$ ssh deploy@your_server_ip
```

### Step Seven — Set Up a Basic Firewall

OpenSSH, the service allowing us to connect to our server now, has a profile registered with UFW.

You can see this by typing:

```
$ sudo ufw app list
```

```
Output
Available applications:
  OpenSSH
```

We need to make sure that the firewall allows SSH connections so that we can log back in next time. We can allow these connections by typing:

```
$ sudo ufw allow OpenSSH
```

Afterwards, we can enable the firewall by typing:

```
$ sudo ufw enable
```

View ufw status:

```
$ sudo ufw status
```
```
Output
Status: active

To                         Action      From
--                         ------      ----
OpenSSH                    ALLOW       Anywhere
OpenSSH (v6)               ALLOW       Anywhere (v6)
```