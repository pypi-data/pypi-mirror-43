import inspect
import unittest
from pyquilted.app_factory import *
from pyquilted.quilted.style import Style


class MockArgs():
    def __init__(self):
        self.one = 1


class TestAppFactory(unittest.TestCase):
    def test_app_factory(self):
        factory = AppFactory(MockArgs())

        self.assertTrue(hasattr(factory, 'args'))
        self.assertTrue(hasattr(factory, 'options'))
        self.assertTrue(hasattr(factory, 'style'))

        self.assertTrue(isinstance(factory.args, dict))
        self.assertTrue(isinstance(factory.style, dict))
        self.assertTrue(isinstance(factory.options, Options))

        self.assertTrue(inspect.ismethod(factory.create))


if __name__ == '__main__':
    unittest.main()
