import json


##
#CONSTANTS

CSV_HEADER = ['Município', 'Poder', 'Problema', 'api', 'periodo', 'url', 'teste']


def digest(data):

    rows = [CSV_HEADER]
    rows += _build_rows(data)

    return rows


##
#UTILS

def _build_rows(data):

    rows = []
    for result in data:

        profile = result['profile']
        tests = result['test_results']

        issues = []
        issues += [_build_row(profile, test, 'dado inacessível') for test in tests['inacessible']]
        issues += [_build_row(profile, test, 'ausência de dados') for test in tests['lack_of_data']]
        issues += [_build_row(profile, test, 'dados falsos') for test in tests['fake_data']]

        rows += issues if len(issues) > 0 else [_build_row(profile)]

    rows = sorted(rows, key=lambda row: ''.join(row))
    return rows

def _build_row(profile, test=None, test_name=None):
    row = [profile['municipio'], profile['poder']]

    if test:
        row += [test_name, test['api'], '{}/{}'.format(test['ano'], test['mes']), test['url'], json.dumps(test)]
    else:
        row += ['nenhum'] + [''] * 4

    return row
