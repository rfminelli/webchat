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

class WebService:

    def __init__(self):
        self.MKAUTH_URL = 'https://10.10.10.10'
        self.MKAUTH_LOGIN = 'admin'
        self.MKAUTH_SENHA = '123'

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
            #print('request login', url_login)
            br.open(url_login)
            br.select_form(name="form")
            br.find_control("login").readonly = False
            br.find_control("senha").readonly = False
            br['login']=base64.b64encode(self.MKAUTH_LOGIN) #use the proper input type=text name
            br['senha']=hashlib.sha256(self.MKAUTH_SENHA).hexdigest() #use the proper input type=password name
            br.submit()

            url = "%s/admin/cliente_det.php?%s" %(self.MKAUTH_URL,urllib.urlencode({'login':kwargs.get('login')}))
            br.open(url)
            page_content = br.response().read()
            soup = BeautifulSoup(page_content,'lxml')
            link_boleto = None
            links_principais = soup.findAll("tr",id="pedro")
            for row in links_principais:
                col = row.findAll('td')
                for c in col:
                    if 'abremostra_mais_carne' in str(c):
                        codigo_carne = str(c).split("abremostra_mais_carne('")[1].split("')")[0]
                        if codigo_carne:

                            carne_url = "%s/admin/mais_carne.php?carne=%s&%s" %(self.MKAUTH_URL,codigo_carne,urllib.urlencode({'login':kwargs.get('login')}))
                            br.open(carne_url)
                            page_content = br.response().read()
                            soup = BeautifulSoup(page_content,'lxml')
                            detalhes_carne = soup.findAll("tr",id="pedro")
                            for row2 in detalhes_carne:
                                col2 = row2.findAll('td')
                                for c2 in col2:
                                    print(c2)






#s = WebService()
#s.run('',login='GIRLEUDA')


