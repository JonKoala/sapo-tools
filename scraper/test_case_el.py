import datetime
from module_el import ModuleEl

class TestCaseEl:

    def __init__(self, root, poder, cases):
        self.module = ModuleEl(root, poder)
        self.root = self.module.root
        self.poder = poder
        self.cases = cases

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

        date_args = self._generate_dates_arguments(self.cases)

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

    def _generate_dates_arguments(self, cases):
        today = datetime.date.today()

        arguments = []
        for case in cases:
            date = datetime.date(case[0], case[1], 1)
            valid = date < today
            arguments += [dict(ano=date.year, mes=date.month, valid_date=valid)]

        return arguments
