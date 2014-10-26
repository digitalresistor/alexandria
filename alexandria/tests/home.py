import unittest
import transaction

from pyramid import testing

class TestHome(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_it(self):
        from ..views.home import home 
        request = testing.DummyRequest()
        info = home(request)
        self.assertEqual(info['info'], 'alexandria')

