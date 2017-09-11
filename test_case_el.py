import datetime
from module_el import ModuleEl

class TestCaseEl:

    def __init__(self, root, poder):
        self.module = ModuleEl(root, poder)
        self.root = self.module.root
        self.poder = poder


TODAY = datetime.date.today()

test = ModuleEl('http://novavenecia-es.portaltp.com.br/', 'executivo')
print(test.request(test.available_urls['pagamentos'], 2017, 1))
