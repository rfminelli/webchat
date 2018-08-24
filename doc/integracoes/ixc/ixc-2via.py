# -*- coding: utf-8 -*-

import re
import requests
import json
import sys

class WebService:

    def __init__(self):
        self.TOKEN = 'TOKEN_AQUI'
        self.WS_HOST = 'http://10.10.10.10'
        self.WS_PATH = '/webservice/v1/fn_areceber/'
        self.WS_URL = '%s%s' %(self.WS_HOST,self.WS_PATH)

    def updatews(self,data_json):
        if data_json.get('TOKEN'):
            self.TOKEN = data_json.get('TOKEN')
        if data_json.get('WS_URL'):
            self.WS_URL = data_json.get('WS_URL')
        if data_json.get('WS_HOST'):
            self.WS_URL = '%s%s' %(data_json.get('WS_HOST'),self.WS_PATH)

    def run(self,q,**kwargs):
        
        reload(sys)
        sys.setdefaultencoding('utf-8')
        
        datareq={}

        data_json = {}
        try:
            data = kwargs.get('data')
            data_json = json.loads(data)
        except:
            pass
        if data_json:
            datareq['cpfcnpj'] = data_json.get('cpfCnpj')
            datareq['contrato'] = data_json.get('contratoId')
            resposta = ''

            self.updatews(data_json)
            datareq['token'] = self.TOKEN
            datareq['app'] = self.APP

            r = requests.post(self.WS_URL,data=datareq)
            rws = r.json()
            if rws.get('link'):
                resposta += '\nLink do boleto: %s' %rws.get('link')
            else:
                resposta += u'\nNão localizamos fatura em aberto para envio do link'
            return {'message': resposta}
        else:
            return {'message': 'Erro no processamento. Favor identifique-se novamente digitando a opção #ajuda'}

