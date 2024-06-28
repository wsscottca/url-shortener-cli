''' Module to run the tests '''
from app.tests.list import test_list
from app.tests.login import test_login
from app.tests.lookup import test_lookup
from app.tests.shorten import test_shorten

def tests():
    ''' Tests all commands '''
    test_login()
    test_shorten()
    test_list()
    test_lookup()
