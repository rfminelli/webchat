# -*- coding: utf-8 -*-

import re
import requests
import json
import sys
import psycopg2
import psycopg2.extras

class WebService:

    def __init__(self):
        self.DB_HOST = '10.10.10.10'
        self.DB_USER = 'usuario_leitura'
        self.DB_PASS = 'senha_usuario_leitura'
        self.DB_NAME = 'mkData3.0'

        self.QUERY = """
select 
pessoa.codpessoa,
contrato.codcontrato,
pessoa.nome_razaosocial,
case when pessoa.cpf is not null then pessoa.cpf else pessoa.cnpj end as cpfcnpj,
pessoa.email,
contrato.suspenso_dt,
contrato.comodato

FROM mk_pessoas pessoa
INNER JOIN mk_cidades cidade ON (cidade.codcidade=pessoa.codcidade)
INNER JOIN mk_cidades cidadecob ON (cidadecob.codcidade=pessoa.codcidadecobranca)
INNER JOIN mk_logradouros logradouro ON (logradouro.codlogradouro=pessoa.codlogradouro)
INNER JOIN mk_logradouros logradourocob ON (logradourocob.codlogradouro=pessoa.codlogradourocobranca)
INNER JOIN mk_bairros bairro ON (bairro.codbairro=pessoa.codbairro)
INNER JOIN mk_bairros bairrocob ON (bairrocob.codbairro=pessoa.codbairrocobranca)
INNER JOIN mk_estados estado ON (estado.codestado=pessoa.codestado)
INNER JOIN mk_estados estadocob ON (estadocob.codestado=pessoa.codestadocobranca)
INNER JOIN mk_contratos contrato ON (contrato.cliente=pessoa.codpessoa) 
LEFT JOIN mk_conexoes conexao ON (conexao.contrato=contrato.codcontrato)
WHERE pessoa.cpf='%s' or pessoa.cnpj='%s'
ORDER BY pessoa.nome_razaosocial
"""
    def dbquery(self, sql, select=True):
        try:
            conn = psycopg2.connect(self.dburi)
        except:
            raise Exception("I am unable to connect to the database")
        if select:
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        else:
            cur = conn.cursor()
        conn.set_client_encoding('UTF8')
        cur.execute(sql)
        if select:
            rows = cur.fetchall()
            conn.close()
            return rows
        else:
            conn.commit()
            conn.close()

    def responseContrato(self,rws,**kwargs):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        response = {}
        response['codcontrato'] = str(rws.get('codcontrato'))
        response['codpessoa'] = str(rws.get('codpessoa'))
        response['nome_razaosocial'] = str(rws.get('nome_razaosocial'))
        response['cpfcnpj'] = str(rws.get('cpfcnpj'))
        response['suspenso'] = len(rws.get('suspenso_dt')) > 0
        response['message'] = u'Olá %s, seja bem-vindo ao autoatendimento. Seguem as opções.' %response['razaoSocial']
        response['customer'] = response['nome_razaosocial']
        response['doc'] = response['cpfcnpj']

        return response

    def run(self,q,**kwargs):

        query = re.sub('[^0-9 ]','',' '.join(q.strip().split()))

        if query:
            datareq={}
            try:
                datareq['cpfcnpj'] = query.split()[0]
            except:
                datareq['cpfcnpj'] = ''

            r = self.dbquery(self.QUERY %(datareq['cpfcnpj'],datareq['cpfcnpj']))
            contrato = None
            if r:
                if len(r) == 1:
                    return self.responseContrato(r)
                else:
                    if len(r) > 1:
                        for c1 in r:
                            if query.split()[1].strip() == str(c1.get('codcontrato')):
                                return self.responseContrato(c1)

                    mensagem = u"Olá %s, verificamos que há mais de 1 contrato." %(rws.get('contratos')[0].get('razaoSocial'))
                    for c1 in r:
                        mensagem += "\n Digite %s %s para selecionar contrato %s" %(query.split()[0],c1.get('codcontrato'),c1.get('codcontrato'))
                    return {'message': mensagem}
            else:
                return {'message': 'Não localizamos o cliente com as informações informadas'}

        return {'message': 'Digite CPF/CNPJ do Assinante'}

