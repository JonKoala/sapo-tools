import json
import csv
from pprint import pprint


##
#constants

CSV_HEADER = ['Município', 'Poder', 'Problema', 'api', 'periodo', 'url', 'teste']

FILE_RESULTS_NAME = 'assets/results'
FILE_SUMMARY_NAME = 'assets/summary'


##
#main

def get_results():
    with open('{}.json'.format(FILE_RESULTS_NAME), 'r') as file_ref:
        return json.load(file_ref)

def build_row(profile, test=None, test_name=None):
    row = [profile['municipio'], profile['poder']]
    row += [test_name, test['api'], '{}/{}'.format(test['ano'], test['mes']), test['url'], json.dumps(test)] if test else ['nenhum'] + [''] * 4

    return row

def output_summary(rows):
    with open('{}.csv'.format(FILE_SUMMARY_NAME), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(CSV_HEADER)
        writer.writerows(rows)


##
#routine

results = get_results()

rows = []
for result in results:

    profile = result['profile']
    tests = result['test_results']

    issues = []
    issues += [build_row(profile, test, 'dado inacessível') for test in tests['inacessible']]
    issues += [build_row(profile, test, 'ausência de dados') for test in tests['lack_of_data']]
    issues += [build_row(profile, test, 'dados falsos') for test in tests['fake_data']]

    rows += issues if len(issues) > 0 else [build_row(profile)]

rows = sorted(rows, key=lambda row: ''.join(row))

output_summary(rows)
