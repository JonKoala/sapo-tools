import re
import csv
import json
import logging
from inspect import getframeinfo, stack
from test_case_el import TestCaseEl


##
#constants

TEST_CASES = [(2016, 4), (2016, 5), (2016, 6), (2016, 7), (2016, 8), (2016, 9), (2016, 10), (2016, 11), (2016, 12), (2017, 1), (2017, 2), (2017, 3)]

FILE_SOURCE_NAME = 'assets/source'
FILE_RESULTS_NAME = 'assets/results'

REGEX_GET_URL = 'http.+portaltp.+\.br'


##
#main

def get_input_csv():

    data = []
    with open('{}.csv'.format(FILE_SOURCE_NAME), 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)  #skipping the header
        for row in reader:
            url_executivo = re.search(REGEX_GET_URL, row[2])
            if url_executivo:
                data += [dict(municipio=row[0],poder='executivo',url=url_executivo[0])]

            url_legislativo = re.search(REGEX_GET_URL, row[4])
            if url_legislativo:
                data += [dict(municipio=row[0],poder='legislativo',url=url_legislativo[0])]

    return data

def execute_tests(input_data):
    test_case = TestCaseEl(input_data['url'], input_data['poder'], TEST_CASES)
    return test_case.execute_full_routine()

def output_result(result):
    text = json.dumps(result)

    with open('{}.json'.format(FILE_RESULTS_NAME), 'w') as file_ref:
        file_ref.write(text)


##
#utils

def log(message, error=False):

    print(message)

    #getting caller data
    caller = getframeinfo(stack()[1][0])
    data = '[{}:{}] {}'.format(caller.filename, caller.lineno, message)

    log_ref = logging.exception if error else logging.info
    log_ref(data)


##
#routine

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.DEBUG,
    filename='assets/log.txt')

log('\n - starting new scraper routine -')

log('extracting data from source (\'{}.csv\')'.format(FILE_SOURCE_NAME))
input_data = get_input_csv()
log('done extracting data ({} test cases)'.format(len(input_data)))

log('executing test routines')
results = []
for index, data in enumerate(input_data):
    try:
        log('testing {}th case ({} - {})'.format(index+1, data['municipio'], data['poder']))
        result = execute_tests(data)
        result['profile'] = data
        results += [result]
    except:
        log('failed testing {}th case ({} - {})'.format(index+1, data['municipio'], data['poder']), True)
log('done executing test routines')

log('printing results to file (\'{}.json\')'.format(FILE_RESULTS_NAME))
output_result(results)
log('done printing results to file')

log('\n - ending scraper routine - \n')
