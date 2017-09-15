import json
from test_case_el import TestCaseEl

import pprint

TEST_MONTH_RADIUS = 6
TEST_PN_CASES = 3

FILE_REPORT_NAME = 'result'

def get_input_data():
    #TODO: pegar os dados de alguma fonte externa

    return [
        dict(municipio='Ponto Belo',poder='executivo',url='http://pontobelo-es.portaltp.com.br/')
        ,dict(municipio='Ponto Belo',poder='legislativo',url='http://cmpontobelo-es.portaltp.com.br/')
    ]

def execute_tests(input_data):
    test_case = TestCaseEl(input_data['url'], input_data['poder'], TEST_PN_CASES, TEST_MONTH_RADIUS)
    return test_case.execute_full_routine()

def output_result(result):
    text = json.dumps(result)

    file_ref = open('{}.json'.format(FILE_REPORT_NAME), 'w')
    file_ref.write(text)
    file_ref.close()

input_data = get_input_data()

results = []
for data in input_data:
    result = execute_tests(data)
    result['fonte'] = data
    results += [result]

output_result(results)
print('end')
