import requests
import datetime
import json
import xml.etree.ElementTree as etree

from scraper.el import model

class Module:

    def __init__(self, root, poder):
        self.model = model.Model(root)
        self.root = self.model.root
        self.poder = poder
        self.available_urls = self.__define_available_urls(self.model)

    def __define_available_urls(self, model):
        available_urls = {
            'servidores': model.GET_URL_SERVIDORES,
            'pagamentos': model.GET_URL_PAGAMENTOS,
            'liquidacoes': model.GET_URL_LIQUIDACOES,
            'empenhos': model.GET_URL_EMPENHOS
        }
        if self.poder == 'executivo':
            available_urls['execucao receitas'] = model.GET_URL_EXECUCAO_RECEITAS

        return available_urls

    def build_url(self, url, ano, mes):
        return '{}?ano={}&mes={}'.format(url, ano, mes)

    def extract_response_data(self, response):
        tree = etree.fromstring(response.text)
        return json.loads(tree.text)

    def request(self, url, ano, mes):
        url = self.build_url(url, ano, mes)
        response = requests.get(url, verify=False)
        status = response.status_code

        result = dict(url=url, status=status)
        #result['data'] = self.extract_response_data(response) if status == 200 else None
        result['registers'] = len(self.extract_response_data(response)) if status == 200 else None

        return result

requests.packages.urllib3.disable_warnings()
