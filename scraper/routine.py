import re

import inout
import digester
from appconfig import settings
from scraper import factory
from logger import log


##
#CONSTANTS

SOURCE_FILE = 'source.csv'
OUTPUT_FOLDER = 'output'
RAW_RESULT_FILE = OUTPUT_FOLDER + '/results.json'
DIGESTED_RESULT_FILE = OUTPUT_FOLDER + '/results.csv'


def filter_source_data(source, model_regex):

    source_data = []
    for row in source:
        url_executivo = re.search(model_regex, row[2])
        if url_executivo:
            source_data += [dict(municipio=row[0],poder='executivo',url=url_executivo[0])]

        url_legislativo = re.search(model_regex, row[4])
        if url_legislativo:
            source_data += [dict(municipio=row[0],poder='legislativo',url=url_legislativo[0])]

    return source_data


##
#ROUTINE

#prep
test_cases = settings['dates']
EL_Tester = factory.get_tester('el')

log('\n - starting new scraper routine -')

log('extracting data from source (\'{}\')'.format(SOURCE_FILE))
raw_csv_input = inout.read_csv(SOURCE_FILE)
el_csv_input = filter_source_data(raw_csv_input, EL_Tester.MODEL_REGEX)
log('done extracting data ({} test cases)'.format(len(el_csv_input)))

log('executing test routines')
results = []
for index, data in enumerate(el_csv_input):
    try:
        log('testing {}th case ({} - {})'.format(index+1, data['municipio'], data['poder']))
        tester = EL_Tester(data['url'], data['poder'], test_cases) #for now we only have EL as a test case
        result = tester.execute_full_routine()
        result['profile'] = data
        results += [result]
    except:
        log('failed testing {}th case ({} - {})'.format(index+1, data['municipio'], data['poder']), logtype='exception')
log('done executing test routines')

log('printing raw results to file (\'{}\')'.format(RAW_RESULT_FILE))
inout.write_json(RAW_RESULT_FILE, results)

log('digesting results')
digested = digester.digest(results)

log('printing digested results to file (\'{}\')'.format(DIGESTED_RESULT_FILE))
inout.write_csv(DIGESTED_RESULT_FILE, digested)


log('\n - ending scraper routine - \n')
