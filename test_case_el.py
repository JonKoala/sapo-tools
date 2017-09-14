import datetime
import random
from dateutil.relativedelta import relativedelta
from module_el import ModuleEl

import pprint

class TestCaseEl:

    def __init__(self, root, poder, cases=3, month_limit=6):
        self.module = ModuleEl(root, poder)
        self.root = self.module.root
        self.poder = poder
        self.cases = cases
        self.month_limit = month_limit

    def execute_requests(self):

        #TODO: pensar se passo esses parametros ou deixo no self mesmo
        date_args = self._generate_dates_arguments(self.cases, self.cases, self.month_limit)

        apis = list(self.module.available_urls)

        results = []
        for api in apis:
            for args in date_args:
                result = self.execute_request(api, args)
                results.append({**args, **result, **dict(api=api)})

        return results

    def execute_request(self, api, args):
        return self.module.request(self.module.available_urls[api], args['ano'], args['mes'])

    def _generate_dates_arguments(self, valid, invalid, month_limit):
        arguments = []

        valid_dates = self._generate_dates(valid, month_limit, False)
        invalid_dates = self._generate_dates(invalid, month_limit, True)

        arguments += [dict(mes=date.month, ano=date.year, valid_date=True) for date in valid_dates]
        arguments += [dict(mes=date.month, ano=date.year, valid_date=False) for date in invalid_dates]

        return arguments

    def _generate_dates(self, count, month_limit, future):
        add_months = random.sample(range(1, month_limit+1), count)
        add_months = [month * (1 if future else -1) for month in add_months]
        today = datetime.date.today()

        dates = [today + relativedelta(months=months) for months in add_months]

        return dates

test = TestCaseEl('http://novavenecia-es.portaltp.com.br/', 'executivo')
#pprint.pprint(test._generate_dates_arguments(3, 3, 6))
pprint.pprint(test.execute_requests())
#print(test.execute_request('pagamentos', dict(ano=2017, mes=6)))
#print(test.build_random_date(future=True))
#print(test.module.request(test.module.available_urls['pagamentos'], 2017, 1))
