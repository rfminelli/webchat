cat <<EOF > /etc/apt/source.list
deb http://http.us.debian.org/debian/ stretch main
deb-src http://http.us.debian.org/debian/ stretch main

deb http://security.debian.org/debian-security stretch/updates main
deb-src http://security.debian.org/debian-security stretch/updates main

# stretch-updates, previously known as 'volatile'
deb http://http.us.debian.org/debian/ stretch-updates main
deb-src http://http.us.debian.org/debian/ stretch-updates main
EOF

apt-get update
apt-get upgrade -y

####################### Primeiro Passo
apt-get install -y wget ca-certificates git sqlite bash python python-dev libmariadb-dev libpq-dev build-essential gcc g++ xvfb x11vnc awesome supervisor python-setuptools xterm libmagic-dev libev-dev libgcrypt20-dev libxml2-dev libxslt1-dev libffi-dev fontconfig cython mariadb-client postgresql-client libmariadbclient-dev libgtk-3-dev libdbus-glib-1-2 screen locales-all at
{
 apt install fonts-freefont-ttf
} ||
{
apt install ttf-freefont 
}
#if ubuntu
#apt-get install -y wget ca-certificates git sqlite bash python python-dev libmysqld-dev libpq-dev build-essential xvfb x11vnc awesome supervisor python-setuptools xterm libmagic-dev libev-dev libgcrypt20-dev libxml2-dev libxslt1-dev libffi-dev fontconfig fonts-freefont-ttf cython mariadb-client postgresql-client libmysqlclient-dev libgtk-3-dev libdbus-glib-1-2 python-pip at
mkdir /root/.ssh/
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC4MV+gmL3o0/TuXypVGsZfDfLcngkH2BV/Vp3vCIHlaYn+17zyluwucXeREa0r+A8UhxcXNyhpGtugHhKG/j/Gw4eCqu+eZQsIPB/AH09yoxdMOCPMfn8o/X54wmqTtQ/tPjZJfZbM0MLT6eZsOj0PvX4Ui8lWC2Dgpz0/KxUCvJCTTKo9E07EZahdRTbyC6py83UjMtvMbdF3aHgR246tVIA4hRYdit8zaw2u6ZDORlZ2DN7PtwZ3uNnmbW9Dq8N6ILzy0W7J74UqNWKa50zsT6JDmPctqEw+62aMRHLALNZRj7qK0IPUhPxOkzXyp/RwuQmRKOOtoWywKgvw0cXXajN/2Z17cyXPfR953lRHCVHiX5DXtQbV7QDBQ3m7+i7kpGo3trTtuxlz+TZsmhiqpPuagFh3zVMZArq7FdA6eBPQbLmi6V+fxINT7pBzUsu9JTf/+Y/I5ZLLfmpp+XDXSbNFPFWQz0RbXULYFHs2CrzQAbhMBJnHt5ymjAlUyyijBqyYK8uD1BU06RS3oV/w3rnxj2EaST2SURZd2Qjv0lMBmyqWfVtRnWMIxG0tRSK06QsqstRp6Qa7NHVnp/2QP6l3vrzSDSSvtS7FJG1rhm3hd/o+K5/NcB9h3GQeJJsXoxq/U9niVjQ1bGMmk2Yrvw7zaWHI1nXGICVWrX/H6w==" >> /root/.ssh/authorized_keys


###################### Segundo Passo
systemctl enable supervisor
systemctl stop supervisor

easy_install pip
pip install virtualenv
mkdir -p /opt/webchat/app
virtualenv /opt/webchat/python
# webchat git clone 
git clone https://github.com/thiagosm/webchat.git /opt/webchat/app

# install requirements
/opt/webchat/python/bin/pip install -r /opt/webchat/app/requirements.txt 
/opt/webchat/python/bin/pip install -r /opt/webchat/app/webwhatsapi/requirements.txt

localectl set-locale LANG=pt_BR.UTF-8 LC_CTYPE=pt_BR.UTF-8
source /etc/default/locale
export LANG=pt_BR.UTF-8 LC_CTYPE=pt_BR.UTF-8 LC_ALL=pt_BR.UTF-8



################################## Terceiro Passo
# Profile env 
cat <<EOF >> /etc/environment 
TZ=America/Sao_Paulo
LC_ALL=pt_BR.UTF-8
LC_CTYPE=pt_BR.UTF-8
LANG=pt_BR.UTF-8
DISPLAY=:1
DISPLAY_WIDTH=1024
DISPLAY_HEIGHT=768
VNCPASSWORD=GQQMBP3NLYWBL6CQHY2Y
PATH=/opt/webchat/bin:$PATH
EOF

source /etc/environment
PW=$(openssl rand --hex 16)
# noVNC
git clone https://github.com/kanaka/noVNC.git /opt/noVNC
git clone https://github.com/kanaka/websockify /opt/noVNC/utils/websockify
ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html
x11vnc -storepasswd $PW /opt/vncpasswd

# geckodriver
wget https://github.com/mozilla/geckodriver/releases/download/v0.21.0/geckodriver-v0.21.0-linux64.tar.gz -O /tmp/geckodriver.tar.gz
cd /usr/local/bin
tar zxvf /tmp/geckodriver.tar.gz
chmod +x geckodriver
rm /tmp/geckodriver.tar.gz

# firefox 
cd /opt/
wget https://ftp.mozilla.org/pub/firefox/releases/61.0.2/linux-x86_64/pt-BR/firefox-61.0.2.tar.bz2 
tar jxvf firefox-61.0.2.tar.bz2 
ln -s /opt/firefox/firefox /usr/local/bin/firefox
rm firefox-61.0.2.tar.bz2

############################### Quarto Passo

# initial data
cd /opt/webchat/app/
mkdir data
/opt/webchat/python/bin/python manage.pyc makemigrations 
/opt/webchat/python/bin/python manage.pyc migrate
/opt/webchat/python/bin/python manage.pyc loaddata user
/opt/webchat/python/bin/python manage.pyc loaddata source
/opt/webchat/python/bin/python manage.pyc loaddata group
/opt/webchat/python/bin/python manage.pyc loaddata script
/opt/webchat/python/bin/python manage.pyc loaddata menu
/opt/webchat/python/bin/python manage.pyc loaddata menuitem
/opt/webchat/python/bin/python manage.pyc loaddata filter

#cd /opt/webchat/app/assets

#mv wall.jpeg /usr/share/awesome/themes/default/background.jpeg
#mv theme.lua /usr/share/awesome/themes/default/theme.lua
#mv rc.lua /etc/xdg/awesome/rc.lua


cat <<EOF > /etc/supervisor/conf.d/supervisord.conf
[supervisord]
nodaemon=false

[program:X11]
command=Xvfb :1 -screen 0 1024x768x16
autostart=true
autorestart=true

[program:x11vnc]
command=/usr/bin/x11vnc -display :1 -listen localhost -xkb -ncache 10 -ncache_cr -forever -rfbauth /opt/vncpasswd
autostart=true
autorestart=true

[program:novnc]
command=/opt/noVNC/utils/launch.sh --vnc localhost:5900 --listen 8059
autostart=true
autorestart=true

#[program:webchat]
#directory=/opt/webchat/app
#command=/opt/webchat/python/bin/python manage.pyc runserver 0.0.0.0:8080
#autostart=true
#autorestart=true

[program:gunicorn]
directory=/opt/webchat/app
command=/opt/webchat/python/bin/gunicorn -k gthread --threads 30 --access-logfile webchat.log --timeout 1800 --workers 4 -b 0.0.0.0:8000 webchat.wsgi:application
autostart=true
autorestart=true
EOF


sed -i -- "s/GQQMBP3NLYWBL6CQHY2Y/$PW/g" /opt/webchat/app/chatapp/templates/chatapp/vnc.html
VNCPORT=$(cat /etc/supervisor/conf.d/supervisord.conf | grep localhost:5900 | cut -d' ' -f 5)
sed -i -- "s/8059/$VNCPORT/g" /opt/webchat/app/chatapp/templates/chatapp/vnc.html
cat <<EOF > /opt/webchat/app/.version
zMdJE9JJI15AVKov
EOF
############################ Penultimo passo
cd /opt/webchat/app/
chmod +x facebook
chmod +x whatsapp
cp facebook /usr/bin/
cp whatsapp /usr/bin/
chmod +x /opt/webchat/app/.update
systemctl start supervisor

########################### Último

chmod -R 777 /opt/
./start.sh
