# -*- coding: utf-8 -*-

import re
import requests
import json
import sys

class WebService:

    def __init__(self):
        self.clientId = '3'
        self.token = None
        self.clientSecret = 'ONe7Ns48Y30tBMzneWAwL6hWuh4ze09Jf7qcMsO9'
        self.username = 'api@hubsoft.com.br'
        self.password = 'api123api'
        self.url = 'https://api.dev.hubsoft.com.br'
        self.urlOauth = '%s/oauth/token' %self.url
        self.urlCliente = '%s/api/v1/integracao/cliente?busca=cpf_cnpj&termo_busca=' %self.url

    def responseContrato(self,rws,**kwargs):
        response = {}
        response['codigo_cliente'] = str(rws.get('codigo_cliente'))
        response['nome_razaosocial'] = str(rws.get('nome_razaosocial'))
        response['cpf_cnpj'] = str(rws.get('cpf_cnpj'))
        response['message'] = u'Olá %s, seja bem-vindo ao autoatendimento. Seguem as opções.' %response['nome_razaosocial']
        response['customer'] = response['nome_razaosocial']
        response['doc'] = response['cpf_cnpj']

        return response

    def run(self,q,**kwargs):

        reload(sys)
        sys.setdefaultencoding('utf-8')

        query = re.sub('[^0-9 ]','',' '.join(q.strip().split()))

        if query:
            requestBody = {}
            requestBody['client_id'] = self.clientId
            requestBody['client_secret'] = self.clientSecret
            requestBody['username'] = self.username
            requestBody['password'] = self.password
            requestBody['grant_type'] = 'password'

            headers = {}
            if self.token:
                headers = {'Authorization': self.token}



            r = requests.post(self.urlOauth,headers=headers,json=requestBody)
            if r.status_code == 200:
                tokenType = r.json().get('token_type')
                accessToken = r.json().get('access_token')
                authorizationToken = '%s %s' %(tokenType,accessToken)
                reqCliente = requests.get('%s%s'%(self.urlCliente,query),
                                                  headers={'Authorization': authorizationToken})
                if reqCliente.status_code == 200:
                    rws = reqCliente.json()
                    if rws.get('clientes'):
                        return self.responseContrato(rws.get('clientes')[0])
                    else:
                        return {'message': 'Não localizamos o cliente com as informações'}
                else:
                    return {'message': 'Falha na integração. '}
            else:
                return {'message': 'Falha na integração. '}

        return {'message': 'Digite CPF/CNPJ do Assinante'}

#s = WebService()
#s.run('09141806654')
