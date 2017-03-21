from unittest import TestCase
import unittest

from app.Amity import Amity
from app.Person import Person, Fellow, Staff
from app.Rooms import Room, Office, LivingSpace
import os


class TestAmity(TestCase):
    def setUp(self):
        amity = Amity()

    def tearDown(self):
        pass
    # Person
    # Test does not add the same person
    # Test changing to an invalid room
    # Test changing an invalid person
    # Test staff cannot change room to a livingspace
    # Test changing office
    # Test staff cannot book living space

    # Amity
    # Test total number of people
    # Test total number of rooms
    # Test loads people from file
    # Test does not load invalid format
    # Test does not load inexisting file
    # Test staff cannot want accommodation
    # Test does not add the same room
    # Test prints allocation to file
    # Test does not overwrite existing file
    # Test creates database
    # Test resets database
    # Test checks for existing dbfile
    # Test does not show state with debug off

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

