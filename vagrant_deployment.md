# Vagrant VM Windows 10 Deployment Tutorial

## Requirements
- Windows 10 version: 10.0.19045 Build 19045
- Oracle VirtualBox (https://www.virtualbox.org/)

### Vagrant Installation
If you encounter an issue with Windows, you will get a blue screen if you attempt to bring up a VirtualBox VM with Hyper-V enabled.

If you wish to use VirtualBox on Windows, you must ensure that Hyper-V is not enabled on Windows. You can turn off the feature with the following Powershell command for Windows 10.

`Disable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-All`

For Windows 11, you can use an elevated Powershell.

`bcdedit /set hypervisorlaunchtype off`

You can also disable Hyper-V in the Windows system settings.

Right click on the Windows button and select ‘Apps and Features’.
Select Turn Windows Features on or off.
Unselect Hyper-V and click OK.
You might have to reboot your machine for the changes to take effect. More information about Hyper-V can be read here.

Then navigate to the vagrant downloads page: https://developer.hashicorp.com/vagrant/downloads

Download your appropriate version for windows.

## Initializing and Configuring VM

### Vagrantfile
```
Vagrant.configure("2") do |config|
  # Ubuntu 22.04 LTS (Jammy)
  config.vm.box = "ubuntu/jammy64"

  # Unique name for VM
  config.vm.define "microblog"

  # VM settings
  config.vm.provider "virtualbox" do |vb|
    vb.name = "microblog"
    vb.memory = "2048"
    vb.cpus = 1
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  end

  # Port forwarding (host:guest)
  config.vm.network "forwarded_port", guest: 5000, host: 5000 # Flask dev server
  config.vm.network "forwarded_port", guest: 80, host: 8080 # Nginx production
  config.vm.network "forwarded_port", guest: 443, host: 8443

  # Sync project folder
  config.vm.synced_folder ".", "/vagrant", type: "virtualbox"
end
```

Copy the above highlighted content and in a new empty directory create a new file called *Vagrantfile*. Then paste into the file, save and close.

### Run VM and setup config

1. Run the command `vagrant up` while in the same directory as the Vagrantfile you created earlier.

2. You can verify that the VM is running with the command `vagrant status` or by opening VirtualBox.

3. Once the VM is up and running, enter the command `vagrant ssh` to ssh into it.

4. To secure your server run the following command to edit sshd_config, `sudo nano /etc/ssh/sshd_config`, then find the lines that start with the following text and change them accordingly:

- `#PermitRootLogin ...` --> `PermitRootLogin no`
- `#PasswordAuthentication ...` --> `PasswordAuthentication no`

Then save and close the file with `Ctrl+O`,`Enter`,`Ctrl+X`.

5. Finally enter the command `sudo service ssh restart`.

### Correcting DNS settings
By default when you create the VM with the environment in this tutorial, you will not be able to access internet through the VM by default, due to DNS settings. To fix this follow the steps below:

1. Edit the resolved configuration:
`sudo nano /etc/systemd/resolved.conf`

2. Add or uncomment the DNS servers:
```
[Resolve]
DNS=8.8.8.8 8.8.4.4
FallbackDNS=1.1.1.1 1.0.0.1
```

3. Restart systemd-resolved:
`sudo systemctl restart systemd-resolved` 

4. Verify:
`resolvectl status`
You should see 8.8.8.8 and 8.8.4.4 as the DNS servers.

5. Then edit the Netplan config:
`sudo nano /etc/netplan/50-cloud-init.yaml`
Modify it to look like this:
```
network:
    version: 2
    ethernets:
        enp0s3:
            dhcp4: true
            nameservers:
                addresses: [8.8.8.8, 8.8.4.4]
```
Then apply the changes:
`sudo netplan apply`
Verify:
`resolvectl status`

6. Now test for internet connectivity:
`ping -c 4 google.com`
If everything works, then you should get ping results

7. Lastly, halt the VM and start it again to see if settings persist.
```
exit
vagrant halt
vagrant up
vagrant ssh
ping -c 4 google.com
```

## Installing apps and dependencies
1. Run the following commands in the VM session to configure the Unified Firewall:
```
sudo apt-get install -y ufw
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow 443/tcp
sudo ufw --force enable
sudo ufw status
```

2. Now run the following commands to install dependencies microblog dependencies:
```
sudo apt-get -y update
sudo apt-get -y install python3 python3-venv python3-dev
sudo apt-get -y install mysql-server postfix supervisor nginx 
```

Use default settings for the installation of each package, and for Postfix select 'Internet' and 'microblog' as the FQDN for Postfix.

## Installing the Microblog Application
1. Run the following commands to clone the microblog repository:
```
cd ~
git clone https://github.com/navidr08-hub/microblog.git
```
2. Set up the python environment:
```
cd ~/microblog
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Install last few python dependencies:
`pip install gunicorn pymysql cryptography`

4. Create the `.env` file for environment variables, it should have the following template:
```
SECRET_KEY=
MAIL_SERVER=
MAIL_PORT=
MAIL_USE_TLS=
MAIL_PASSWORD=
DATABASE_URL=
MS_TRANSLATOR_KEY=
MS_TRANSLATOR_REGION=
# ELASTICSEARCH_URL=
```
You generate a secret key in the terminal with the command:
`python3 -c "import uuid; print(uuid.uuid4().hex)"`

5. Compile language translations:
`flask translate compile`

## Setting up MySQL Database
1. Create the database and user.
```
sudo mysql -u root
create database microblog character set utf8 collate utf8_bin;
create user 'microblog'@'localhost' identified by '<db-password>'; (Replace <db-password> with the same password you are using in the .env file DATABASE_URL=)
grant all privileges on microblog.* to 'microblog'@'localhost';
flush privileges;
quit;
```

2. Run database migrations:
`flask db upgrade`

## Set up Gunicorn and Supervisor
1. Start editing the supervisor config file with:
`sudo nano /etc/supervisor/conf.d/microblog.conf`

2. Paste the following text into the file:
```
[program:microblog]
command=/home/vagrant/microblog/venv/bin/gunicorn -b 127.0.0.1:5000 -w 4 microblog:app
directory=/home/vagrant/microblog
user=vagrant
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stdout_logfile=/var/log/microblog_stdout.log
stderr_logfile=/var/log/microblog_stderr.log
environment=PATH="/home/vagrant/microblog/venv/bin",HOME="/home/vagrant"
```
Then save and close the file with `Ctrl+O`,`Enter`,`Ctrl+X`.

3. Finally reload the supervisor service:
`sudo supervisorctl reload`

## Set up Nginx
1. Create the self-signed SSL certificate:
```
cd ~/microblog
mkdir certs
openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 \
  -keyout certs/key.pem -out certs/cert.pem
```

2. Edit the nginx config file:
`sudo nano /etc/nginx/sites-available/microblog`

### Optional: Make the Web-App "Secure" with HTTPS
3. Paste the following contents into the file:
```
server {
    listen 80;
    server_name _;
    location / {
        # redirect any requests to the same URL but on https
        return 301 https://$host$request_uri;
    }
}
server {
    # listen on port 443 (https)
    listen 443 ssl;
    server_name _;

    # location of the self-signed SSL certificate
    ssl_certificate /home/vagrant/microblog/certs/cert.pem;
    ssl_certificate_key /home/vagrant/microblog/certs/key.pem;

    # write access and error logs to /var/log
    access_log /var/log/microblog_access.log;
    error_log /var/log/microblog_error.log;

    location / {
        # forward application requests to the gunicorn server
        proxy_pass http://localhost:5000;
        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        # handle static files directly, without forwarding to the application
        alias /home/vagrant/microblog/app/static;
        expires 30d;
    }
}
```
Then save and close the file with `Ctrl+O`,`Enter`,`Ctrl+X`.

### HTTP Deployment
This is if you do not want to deploy "secure" with HTTPS
3. Paste the following content into the file:
```
server {
    listen 80;
    server_name _;

    access_log /var/log/microblog_access.log;
    error_log /var/log/microblog_error.log;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/vagrant/microblog/app/static/;
        expires 30d;
        add_header Cache-Control "public";
    }
}
```
Then save and close the file with `Ctrl+O`,`Enter`,`Ctrl+X`.


4. Create a link to the nginx config in sites-enabled:
```
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s /etc/nginx/sites-available/microblog /etc/nginx/sites-enabled/microblog
sudo service nginx reload
```

## Test the Application

All deployment steps are complete, all thats left is to test the application, to verify functionality.

1. Test Authentication
- User Registration
 - Create basic user in regular use case ... Done
 - Enter problematic text in fields ... 

- User login ... Done

- Password Reset ...

2. Test Posts and Profile
- Post something ... Done
- Translate a post ... Done
- Change about me in Profile ... Done
- Change username ... Done

3. Test Explore ...