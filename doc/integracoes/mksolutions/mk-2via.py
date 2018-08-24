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
select p.codcliente_codfornecedor as cliente,  
       p.codvinculado as contrato,
       b.cod_cedente,      
       p.descricao_conta as demonstrativo,
       p.data_lancamento as emissao,
       p.data_vencimento as vencimento,
       p.data_liquidacao as pagamento,
       b.nosso_numero as numero_documento,
       b.nosso_numero as nosso_numero,
       --b.valor_cobrado as valor,
       f.valor_total as valor,
       f.vlr_liquidacao as valorpago,
       b.codconta,
       b.cod_cedente,
       f.suspenso,
       f.data_suspensao,
       f.excluida,
       b.substituido
from mk_plano_contas p 
inner join mk_contas_faturadas cf on (cf.cd_conta=p.codconta)
inner join mk_faturas f on (f.codfatura=cf.cd_fatura and f.data_exclusao is null)
inner join mk_boletos_gerados b on (b.cd_fatura=cf.cd_fatura or b.codconta=p.codconta)
where p.codvinculado = %s
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
                datareq['codcontrato'] = query.split()[0]
            except:
                datareq['codcontrato'] = ''

            r = self.dbquery(self.QUERY %(datareq['codcontrato']))
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

