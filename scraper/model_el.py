import requests
import datetime
import json
import xml.etree.ElementTree as etree

class ModelEl:

    #documentation: self.root + '/api/dadosabertos.aspx'
    GET_URL_MODEL = '{}api/transparencia.asmx/{}'

    def __init__(self, root):
        self.root = self.__format_root(root)

    def __format_root(self, root):
        prefix = '' if root[:4] == 'http' else 'http://'
        suffix = '' if root[-1:] == '/' else '/'
        return prefix + root.replace('https', 'http') + suffix

    def __format_get_url(self, url_ending):
        return self.GET_URL_MODEL.format(self.root, url_ending)

    @property
    def GET_URL_SERVIDORES(self): return self.__format_get_url('json_servidores')

    @property
    def GET_URL_PAGAMENTOS(self): return self.__format_get_url('json_pagamentos')

    @property
    def GET_URL_LIQUIDACOES(self): return self.__format_get_url('json_liquidacoes')

    @property
    def GET_URL_EMPENHOS(self): return self.__format_get_url('json_empenhos')

    #legislativo não faz uso
    @property
    def GET_URL_EXECUCAO_RECEITAS(self): return self.__format_get_url('json_execucao_receitas')
