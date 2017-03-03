from unittest import TestCase
import unittest

from app.Amity import Amity
from app.Person import Person, Fellow, Staff
from  app.Rooms import Room, Office, LivingSpace
import os


class TestAmity(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_adds_rooms(self):
        amity = Amity()

        amity.add_room("Mombasa", "O")
        expected_rooms = {"Offices": [{"name": "Mombasa",
                                       "id": 1}],
                          "LivingSpaces": []}
        self.assertDictEqual(expected_rooms, amity.rooms)

        amity.add_room("Pluto", "L")
        expected_rooms = {"Offices": [{"name": "Mombasa",
                                       "id": 2}],
                          "LivingSpaces": [{"name": "Pluto",
                                            "id": 3}
                                           ]}
        self.assertDictEqual(expected_rooms, amity.rooms)

    def test_adds_person(self):
        amity = Amity()

        amity.add_person("Joseph", "F")
        expected_people = {"Staff": [],
                           "Fellows": [{"name": "Joseph",
                                        "id": 1,
                                        "wants_accomodation": False}
                                       ]}
        self.assertDictEqual(expected_people, amity.people)

        amity.add_person("Kalumba Muteo", "S", True)
        expected_people = {"Staff": [{"name": "Kalumba Muteo",
                                      "id": 2}],
                           "Fellows": [{"name": "Joseph",
                                        "id": 3,
                                        "wants_accomodation": True}
                                       ]}
        self.assertDictEqual(expected_people, amity.people)

    def test_adds_total_number_of_people(self):
        amity = Amity()

        amity.add_person("Joseph", "F", True)
        amity.add_person("Letty", "S")
        amity.add_person("Max", "F")
        self.assertEqual(3, amity.total_no_of_people)

    def test_adds_total_number_of_rooms(self):
        amity = Amity()

        amity.add_room("Ergeton", "O")
        amity.add_person("Gibralta", "L")
        self.assertEqual(2, amity.total_no_of_rooms)

    def test_loads_people(self):
        amity = Amity()
        # Create file with people
        file = open("people.txt", "w+")
        file.write("OLUWAFEMI SULE FELLOW Y \r\nDOMINIC WALTERS STAFF \r\n")
        file.close()

        amity.add_room("Egerton", "O")
        amity.add_room("Gibralta", "L")
        amity.load_people("people.txt")
        expected_allocated_rooms = {"Egerton": ["DOMINIC WALTERS","OLUWAFEMI SULE"],
                                    "Gibralta": ["OLUWAFEMI SULE"]}
        os.remove("people.txt")
        self.assertDictEqual(expected_allocated_rooms, amity.allocated_rooms)

    def test_unallocated_people(self):
        amity = Amity()

        amity.add_person("Greg Unitiera", "S")
        amity.add_person("Greg Rets", "F")
        amity.add_person("Bob Unitiera", "S")

        expected_unallocated_people = {"Staff": ["Greg Unitiera", "Bob Unitiera"],
                                       "Fellows": ["Greg Rets"]}
        self.assertDictEqual(expected_unallocated_people, amity.unallocated_people)

    def test_saves_state(self):
        pass

    def test_loads_state(self):
        pass

    # Edge cases.
    # 1. Staff wants accomodation
    def test_staff_cannot_get_livingspace(self):
        amity = Amity()

        self.assertRaises(ValueError, amity.add_person("Sedan Mbuto", "S", True))

    # 2. Bad room type
    def test_bad_room_type(self):
        amity = Amity()

        self.assertRaises(ValueError, amity.add_room("Liberty", "D"))

    # 3. Bad staff type
    def test_bad_staff_type(self):
        amity = Amity()

        self.assertRaises(ValueError, amity.add_person("Franco", "G", False))

    # 3. Similar room names
    def test_similar_room_names(self):
        amity = Amity()

        amity.add_room("Le'Brone", "O")
        self.assertRaises(ValueError, amity.add_room("Le'Brone", "O"))

    # 4. Similar people names gets added
    def test_similar_people_names_not_added(self):
        amity = Amity()

        amity.add_person("Geogreen Otieno", "F")
        self.assertRaises(ValueError, amity.add_person("Geogreen Otieno", "F"))


class TestRoom(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_adds_occupants(self):
        amity = Amity()
        amity.add_room("Kisumu", "O")

        office = Office(amity, "Kisumu")
        office.assign_occupant("David Moyes")
        expected_allocation = {"Kisumu": ["David Moyes"]}

        self.assertDictEqual(expected_allocation, amity.allocated_rooms)

    def test_evacuates_occupants(self):
        amity = Amity()
        amity.allocated_rooms = {"Kisumu": ["David Moyes"]}

        kisumu = Office(amity, "Kisumu")
        kisumu.evacuate_occupant("David Moyes")

        self.assertDictEqual({"Kisumu": []}, amity.allocated_rooms)

    def test_all_occupants(self):
        amity = Amity()
        amity.allocated_rooms = {"Kisumu": ["David Moyes", "Kevin Love"]}

        kisumu = Office(amity, "Kisumu")
        all_occupants = kisumu.show_all_occupants("Kisumu")
        expected_occupants = ["David Moyes", "Kevin Love"]
        self.assertListEqual(expected_occupants, all_occupants)
        self.assertEqual(2, kisumu.no_of_occupants)

    def test_officec_maximum_number_of_occupants(self):
        amity = Amity()
        amity.rooms = {"Offices": [{"name": "Mombasa",
                                    "id": 2}],
                       "LivingSpaces": [{"name": "Pluto",
                                         "id": 3}
                                        ]}

        office = Office(amity, "Mombasa")
        # self.assertEqual(6, office.max_no_of_occupants)
        assert 6 == office.max_no_of_occupants

        dorm = LivingSpace(amity, "Pluto")
        assert 4 == dorm.max_no_of_occupant

        # Assign more than 6 people to an office
        # Assign more than 4 people to a dorm

    def test_assign_or_evacuate_who_doesnt_exist(self):
        amity = Amity()
        amity.rooms = {"Offices": [{"name": "Mombasa",
                                    "id": 2}],
                       "LivingSpaces": [{"name": "Pluto",
                                         "id": 3}
                                        ]}
        amity.allocated_rooms = {"Mombasa": [],
                                 "Pluto": []}
        amity.people = {"Staff": [],
                        "Fellows": []}

        mombasa = Office(amity, "Mombasa")
        self.assertRaises(ValueError, mombasa.evacuate_occupant("Dennis"))
        self.assertRaises(ValueError, mombasa.assign_occupant("Dennis"))


    # Room cannot have two same people at the same time


class TestPerson(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_person_books_room(self):
        pass

    def test_person_evacuates_room(self):
        pass

    def fellow_books_living_space(self):
        pass

    def fellow_evacuates_living_space(self):
        pass


    # 1. Books space with expected changes
    # 2. Evacuates space with expected changes
    # 3. Fellow can book living space with expected changes

