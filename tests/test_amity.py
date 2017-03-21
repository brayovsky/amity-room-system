from unittest import TestCase
import unittest

from app.Amity import Amity
from app.Person import Person, Fellow, Staff
from app.Rooms import Room, Office, LivingSpace
import os


class TestAmity(TestCase):
    def setUp(self):
        self.amity = Amity()

    def tearDown(self):
        pass

    def test_total_number_of_people_increases(self):
        pass

    def test_total_number_of_rooms_increases(self):
        pass

    def test_does_not_load_invalid_file(self):
        pass

    def test_does_not_load_inexisting_file(self):
        pass

    def test_loads_file(self):
        pass

    def test_staff_cannot_want_accommodation(self):
        pass

    def test_does_not_add_person_twice(self):
        pass

    def test_does_not_add_person_twice(self):
        pass

    def test_prints_allocation_to_file(self):
        pass

    def test_does_not_overwrite_existing_file(self):
        pass

    def test_creates_database(self):
        pass

    def test_resets_database(self):
        pass

    def test_checks_for_existing_database(self):
        pass

    def test_does_not_show_state_with_debug_off(self):
        pass
    # Person
    # Test does not add the same person
    # Test changing to an invalid room
    # Test changing an invalid person
    # Test staff cannot change room to a livingspace
    # Test changing office
    # Test staff cannot book living space


    # Room
    # Test adding more than 6 people to a room
    # Test adding more than 4 people to a room


class TestRoom(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


class TestPerson(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass


