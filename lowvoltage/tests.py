from . import services
from django.test import TestCase


class MyTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        pass

    def test1(self):
        # Some test using self.foo
        pass

    def test2(self):
        # Some other test using self.foo
        pass
