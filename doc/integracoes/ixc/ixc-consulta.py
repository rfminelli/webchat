# -*- coding: utf-8 -*-

import re
import requests
import json
import sys

class WebService:
"""
require(__DIR__ . DIRECTORY_SEPARATOR . 'WebserviceClient.php');
$host = 'https://SEU_DOMINIO/webservice/v1';
$token = '6:4dacdb8e47193e8cbbabe508c3c59b4547e463817b1d9b9a1d20ab4812fe1a62';//token gerado no cadastro do usuario (verificar permissões)
$selfSigned = true; //true para certificado auto assinado
$api = new IXCsoft\WebserviceClient($host, $token, $selfSigned);
$params = array(
    'qtype' => 'cliente_contrato.id',//campo de filtro
    'query' => '1',//valor para consultar
    'oper' => '=',//operador da consulta
    'page' => '1',//página a ser mostrada
    'rp' => '20',//quantidade de registros por página
    'sortname' => 'cliente_contrato.id',//campo para ordenar a consulta
    'sortorder' => 'desc'//ordenação (asc= crescente | desc=decrescente)
);
$api->get('cliente_contrato', $params);
$retorno = $api->getRespostaConteudo(false);// false para json | true para array
"""


    def __init__(self):
        self.TOKEN = 'TOKEN_AQUI'
        self.WS_HOST = 'http://10.10.10.10'
        self.WS_PATH = '/webservice/v1/cliente/'
        self.WS_PATH_CONTRATO = '/webservice/v1/cliente_contrato/'
        self.WS_URL = '%s%s' %(self.WS_HOST,self.WS_PATH)

    def responseContrato(self,rws,**kwargs):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        response = {}
        response['id'] = str(rws.get('id'))
        response['razaoSocial'] = str(rws.get('razaoSocial'))
        response['cpfCnpj'] = str(rws.get('cpfCnpj'))
        response['contratoStatus'] = str(rws.get('contratoStatus'))
        response['contratoStatusDisplay'] = str(rws.get('contratoStatusDisplay'))
        response['contratoStatusModo'] = str(rws.get('contratoStatusModo'))
        response['message'] = u'Olá %s, seja bem-vindo ao autoatendimento. Seguem as opções.' %response['razaoSocial']
        response['customer'] = response['razaosocial']
        response['doc'] = response['cnpj_cpf']

        if kwargs.get('next_ws'):
            response['TOKEN'] = self.TOKEN
            response['WS_HOST'] = self.WS_HOST
            response['APP'] = self.APP

        return response

    def run(self,q,**kwargs):

        query = re.sub('[^0-9 ]','',' '.join(q.strip().split()))

        if query:
            datareq={}
            datareq['token'] = self.TOKEN
            datareq['app'] = self.APP
            try:
                datareq['cnpj_cpf'] = query.split()[0]
            except:
                datareq['cnpj_cpf'] = ''

            r = requests.post(self.WS_URL,data=datareq)
            rws = r.json()
            contrato = None
            print(rws)

            #if rws.get('contratos'):
            #    if len(rws.get('contratos')) == 1:
            #        return self.responseContrato(rws.get('contratos')[0])
            #    else:
            #        if len(query.split()) > 1:
            #            for c1 in rws.get('contratos'):
            #                if query.split()[1].strip() == str(c1.get('contratoId')):
            #                    return self.responseContrato(c1,**kwargs)
#
            #        mensagem = u"Olá %s, verificamos que há mais de 1 contrato." %(rws.get('contratos')[0].get('razaoSocial'))
            #        for c1 in rws.get('contratos'):
            #            mensagem += "\n Digite %s %s para selecionar contrato %s" %(query.split()[0],c1.get('contratoId'),c1.get('contratoId'))
            #        return {'message': mensagem}
            #else:
            #    # descomentar abaixo se quiser consultar outros sistemas caso nao encontre o cliente
            #    #if not kwargs.get('next_ws'):
            #    #    # consultar outra empresa 
            #    #    self.TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxx'
            #    #    self.WS_HOST = 'http://XXX.XXX.XXX.XXX:8000'
            #    #    kwargs['next_ws'] = True
            #    #    return self.run(q,**kwargs)
            #    return {'message': 'Não localizamos o cliente com as informações informadas'}

        return {'message': 'Digite CPF/CNPJ do Assinante'}

