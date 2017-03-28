from unittest import TestCase

from app.Amity import Amity


class BaseTestCase(TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.amity = Amity()
        self.amity.total_no_of_rooms = 0
        self.amity.total_no_of_people = 0
        self.amity.total_no_of_offices = 0
        self.amity.total_no_of_livingspaces = 0
        self.amity.rooms = {}
        self.amity.people = {}

    def tearDown(self):
        pass
