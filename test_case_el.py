import datetime
import random
from dateutil.relativedelta import relativedelta
from module_el import ModuleEl

class TestCaseEl:

    def __init__(self, root, poder, cases, month_radius):
        self.module = ModuleEl(root, poder)
        self.root = self.module.root
        self.poder = poder
        self.cases = cases
        self.month_radius = month_radius if cases < month_radius else cases

    def execute_full_routine(self):

        request_results = self.execute_requests()
        inacessible, lack_of_data, fake_data = self.execute_test_battery(request_results)

        return {
            'test_cases' : request_results,
            'test_results' : {
                'inacessible' : inacessible,
                'lack_of_data' : lack_of_data,
                'fake_data' : fake_data
            }
        }

    ##
    #executing tests

    def execute_test_battery(self, results):

        inacessible = []
        lack_of_data = []
        fake_data = []

        for result in results:
            inacessible += [result] if self.test_inaccessibility(result) else []
            lack_of_data += [result] if self.test_lack_of_data(result) else []
            fake_data += [result] if self.test_fake_data(result) else []

        return inacessible, lack_of_data, fake_data

    def test_inaccessibility(self, result):
        return result['status'] != 200

    def test_lack_of_data(self, result):
        return result['valid_date'] and result['registers'] == 0

    def test_fake_data(self, result):
        return not result['valid_date'] and isinstance(result['registers'], int) and result['registers'] > 0

    ##
    #retrieving data

    def execute_requests(self):

        date_args = self._generate_dates_arguments(self.cases, self.cases, self.month_radius)

        apis = list(self.module.available_urls)

        results = []
        for api in apis:
            for args in date_args:
                result = self.execute_request(api, args)
                results.append({**args, **result, **dict(api=api)})

        return results

    def execute_request(self, api, args):
        return self.module.request(self.module.available_urls[api], args['ano'], args['mes'])

    ##
    #arguments generation

    def _generate_dates_arguments(self, valid, invalid, month_radius):
        arguments = []

        valid_dates = self._generate_dates(valid, month_radius, False)
        invalid_dates = self._generate_dates(invalid, month_radius, True)

        arguments += [dict(mes=date.month, ano=date.year, valid_date=True) for date in valid_dates]
        arguments += [dict(mes=date.month, ano=date.year, valid_date=False) for date in invalid_dates]

        return arguments

    def _generate_dates(self, count, month_radius, future):
        add_months = random.sample(range(1, month_radius+1), count)
        add_months = [month * (1 if future else -1) for month in add_months]
        today = datetime.date.today()

        dates = [today + relativedelta(months=months) for months in add_months]

        return dates
