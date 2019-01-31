#!/bin/bash
cd /opt/webchat/app
export TZ=America/Sao_Paulo
export LC_ALL= pt_BR.UTF-8
export LC_CTYPE=pt_BR.UTF-8
export LANG=pt_BR.UTF-8
export DISPLAY=:1
export DISPLAY_WIDTH=1024
export DISPLAY_HEIGHT=768
export VNCPASSWORD=GQQMBP3NLYWBL6CQHY2Y
export PATH=/opt/webchat/bin:$PATH

/usr/bin/awesome&
/usr/bin/xterm -e "/opt/webchat/python/bin/python manage.pyc whatsapp"&
/usr/bin/xterm -e "/opt/webchat/python/bin/python manage.pyc facebook"&
