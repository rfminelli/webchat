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
        self.urlCliente = '%s/api/v1/integracao/cliente/desbloqueio_confianca?id_cliente_servico=' %self.url

    def run(self,q,**kwargs):

        reload(sys)
        sys.setdefaultencoding('utf-8')

        data_json = {}
        try:
            data = kwargs.get('data')
            data_json = json.loads(data)
        except:
            pass

        if data_json.get('codigo_cliente'):

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
                reqCliente = requests.get('%s%s&dias_desbloqueio=1' %(self.urlCliente,data_json.get('codigo_cliente')),
                                                  headers={'Authorization': authorizationToken})
                if reqCliente.status_code == 200:
                    rws = reqCliente.json()
                    resposta = ""
                    if rws.get('success'):                        
                        return {'message': rws.get('msg')}
                    return {'message': 'Desbloqueio não realizado. Entrar em contato com o provedor'}
                return {'message': 'Error na consulta do sistema'}

        return {'message': 'Erro no processamento. Favor identifique-se novamente digitando a opção #ajuda'}


