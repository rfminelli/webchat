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

    def responseContrato(self,rws,**kwargs):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        response = {}
        response.update(rws)

        response['message'] = u'Olá %s, seja bem-vindo ao autoatendimento. Seguem as opções.' %response['nome']
        response['customer'] = response['nome']
        response['doc'] = response['cpfcnpj']

        return response

    def run(self,q,**kwargs):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        query = re.sub('[^0-9 ]','',' '.join(q.strip().split()))

        if query:
            
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

            br.open("%s/admin/clientes.php?tipo=todos&busca=%s&campo=cpf_cnpj&ordem=nenhum&enviar=Buscar" %(self.MKAUTH_URL,query))
            page_content = br.response().read()
            soup  = BeautifulSoup(page_content,'lxml')
            i = 0
            response = []
            cliente = {}
            for col in soup.findAll("font",id="cliente"):
                for c in col:
                    i += 1
                    if i == 1:
                        cliente['login'] = c.strip()
                    elif i == 2:
                        cliente['plano'] = c.strip()
                    elif i == 3:
                        cliente['ip'] = c.strip()
                    elif i == 4:
                        cliente['ramal'] = c.strip()
                    elif i == 5:
                        cliente['nome'] = c.strip()
                        i = 0
                        cliente['cpfcnpj'] = query.split()[0]
                        if cliente.get('login'):
                            link_desbloqueio = 'executar_blo.php?acao=desbloqueio&login=%s\'' %cliente.get('login')
                            if link_desbloqueio in str(soup):
                                cliente['suspenso'] = True
                        response.append(cliente)
                        cliente = {}


            if len(response) == 1:
                return self.responseContrato(response[0])

            elif len(response) > 1:
                if len(query.split()) > 1:
                    for c1 in response:
                        if query.split()[1].strip() == c1['login']:
                            return self.responseContrato(c1)

                mensagem = u"Olá %s, verificamos que há mais de 1 contrato." %(rws.get('contratos')[0].get('razaoSocial'))
                for c1 in response:
                    mensagem += "\n Digite %s %s para selecionar cadastro do login %s" %(query.split()[0],c1.get('login'),c1.get('login'))
                return {'message': mensagem}
            else:
                return {'message': 'Não localizamos o cliente com as informações informadas'}

        return {'message': 'Digite CPF/CNPJ do Assinante'}


#s = WebService()
#c = s.run('CPF OU CNPJ')
#print(c)