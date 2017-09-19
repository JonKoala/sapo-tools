import re
import csv
import json
from test_case_el import TestCaseEl

import pprint

TEST_MONTH_RADIUS = 6
TEST_PN_CASES = 6

FILE_SOURCE_NAME = 'assets/source'
FILE_RESULTS_NAME = 'assets/results'

REGEX_GET_URL = 'http.+portaltp.+\.br'

def get_input_csv():

    data = []
    with open('{}.csv'.format(FILE_SOURCE_NAME), 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter=';')
        for row in rows:

            url_executivo = re.search(REGEX_GET_URL, row[2])
            if url_executivo:
                data += [dict(municipio=row[0],poder='executivo',url=url_executivo[0])]

            url_legislativo = re.search(REGEX_GET_URL, row[4])
            if url_legislativo:
                data += [dict(municipio=row[0],poder='legislativo',url=url_legislativo[0])]

    return data

def execute_tests(input_data):
    test_case = TestCaseEl(input_data['url'], input_data['poder'], TEST_PN_CASES, TEST_MONTH_RADIUS)
    return test_case.execute_full_routine()

def output_result(result):
    text = json.dumps(result)

    with open('{}.json'.format(FILE_RESULTS_NAME), 'w') as file_ref:
        file_ref.write(text)


input_data = get_input_csv()

results = []
for data in input_data:
    result = execute_tests(data)
    result['profile'] = data
    results += [result]

output_result(results)
print('end')
