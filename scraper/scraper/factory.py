import scraper.el as el

_TESTERS = {
    'el': el.tester.Tester
}

def get_tester(model):

    model = model.lower()
    return _TESTERS[model]
