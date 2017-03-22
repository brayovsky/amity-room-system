from unittest import TestCase

from Amity import Amity


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.amity = Amity()


