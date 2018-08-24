#!/usr/bin/python
# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import requests 
import sys
import re
import cookielib
from mechanize import Browser
import mechanize
from bs4 import BeautifulSoup
import base64 
import hashlib
import time 
import mechanize
import ssl
import logging 
import csv
import argparse
import urllib
from datetime import date, timedelta



class WebService:

    def __init__(self):
        self.MKAUTH_URL = 'https://10.10.10.10'
        self.MKAUTH_LOGIN = 'admin'
        self.MKAUTH_SENHA = '123'
        self.MKAUTH_LIBERACAO_DIAS = 1

    def run(self,q,**kwargs):

        query = re.sub('[^0-9 ]','',' '.join(q.strip().split()))

        if kwargs.get('login'):

            logger = logging.getLogger("mechanize")
            logger.addHandler(logging.StreamHandler(sys.stdout))
            logger.setLevel(logging.INFO)

            ssl._create_default_https_context = ssl._create_unverified_context

            br = mechanize.Browser()
            br.set_debug_redirects(True)

            # Cookie Jar
            cj = cookielib.LWPCookieJar()
            br.set_cookiejar(cj)

            # Browser options
            br.set_handle_equiv(True)
            br.set_handle_gzip(True)
            br.set_handle_redirect(True)
            br.set_handle_referer(True)
            br.set_handle_robots(False)

            # Follows refresh 0 but not hangs on refresh > 0
            br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

            # User-Agent (fake agent to google-chrome linux x86_64)
            br.addheaders = [('User-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'),
                             ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                             ('Accept-Encoding', 'gzip,deflate,sdch'),                  
                             ('Accept-Language', 'en-US,en;q=0.8'),                     
                             ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')]

            url_login = '%s/admin/login.php' %self.MKAUTH_URL
            br.open(url_login)
            br.select_form(name="form")
            br.find_control("login").readonly = False
            br.find_control("senha").readonly = False
            br['login']=base64.b64encode(self.MKAUTH_LOGIN) #use the proper input type=text name
            br['senha']=hashlib.sha256(self.MKAUTH_SENHA).hexdigest() #use the proper input type=password name
            br.submit()

            url = "%s/admin/cliente_alt.php?%s" %(self.MKAUTH_URL,urllib.urlencode({'login':kwargs.get('login')}))
            br.open(url)
            br.select_form(name="form")
            br.form['observacao'] = ['sim']
            br.form['rem_obs'] = (date.today() + timedelta(days=self.MKAUTH_LIBERACAO_DIAS)).strftime('%d/%m/%Y')
            br.submit()

            page_content = br.response().read()
            soup  = BeautifulSoup(page_content,'lxml')
            print(soup)

            if 'Dados alterados com sucesso' in str(soup):
                return {'redirect_menu': True, 
                         'message': u'Acesso liberado com sucesso.Em alguns minutos a conexão estará normalizada. Caso não normalize o acesso em 5 minutos, favor desligar e ligar o equipamento.'}
            else:
                return {'redirect_menu':True,
                        'message': u'Erro Interno, tente novamente posteriormente.'}
        else:
            return {'message': u'Erro no processamento. Favor identifique-se novamente digitando a opção #ajuda'}



#s = WebService()
#print(s.run('',login='LOGIN'))


