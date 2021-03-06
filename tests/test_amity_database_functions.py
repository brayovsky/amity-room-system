import os
import unittest

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session

from tests.basetest import BaseTestCase
from app.Model import Base, Allocations, People, Rooms
from app.Person import Fellow, Staff
from app.Rooms import LivingSpace, Office


class TestAmityDatabaseFunctions(BaseTestCase):
    def setUp(self):
        super(TestAmityDatabaseFunctions, self).setUp()
        self.engine = create_engine("sqlite:///test_database.db")
        Base.metadata.create_all(self.engine)
        self.db_session = sessionmaker(bind=self.engine)
        self.session = self.db_session()

    def tearDown(self):
        db_path = os.path.dirname(os.path.realpath(__file__)) + "/../"
        complete_db_path = os.path.join(db_path, "test_database.db")
        os.remove(complete_db_path)

    def test_resets_database(self):
        self.amity.reset_db("test_database.db")

        assert not self.engine.dialect.has_table(self.engine, "rooms")

    def test_checks_for_existing_database(self):
        assert self.amity.check_db_exists("test_database.db")

    def test_connects_to_database(self):
        session = self.amity.connect_to_db("test_database.db")
        person = People(person_name="Joe", person_type="Fellows")
        session.add(person)
        session.commit()
        # Check was added
        person = self.session.query(People.person_name).first()

        self.assertTupleEqual(person, ("Joe", ))

    def test_creates_database(self):
        self.amity.create_database("some_database.db")

        db_path = os.path.dirname(
            os.path.realpath(__file__)) + "/../"

        db_complete_name = os.path.join(db_path, "some_database.db")

        assert os.path.isfile(db_complete_name)

        os.remove(db_complete_name)

    def test_saves_state(self):
        self.amity.people["Dan"] = Fellow("Dan", wants_accommodation=True)
        self.amity.people["Simon"] = Staff("Simon")
        self.amity.rooms["Riverwood"] = Office("Riverwood")
        self.amity.rooms["Java"] = LivingSpace("Java")
        self.amity.total_no_of_rooms = 2
        self.amity.total_no_of_people = 2
        self.amity.total_no_of_livingspaces = 1
        self.amity.total_no_of_offices = 1

        self.amity.people["Dan"].office = "Riverwood"
        self.amity.people["Simon"].office = "Riverwood"
        self.amity.people["Dan"].livingspace = "Java"
        self.amity.rooms["Java"].occupants = {"Dan", }
        self.amity.rooms["Riverwood"].occupants = {"Dan", "Simon"}

        self.amity.save_current_data("test_database.db")

        people = self.session.query(People)
        rooms = self.session.query(Rooms)
        allocated = self.session.query(Allocations)

        amity_people = dict()
        for person in people:
            amity_people[person.person_name] = person.person_type

        self.assertDictEqual(amity_people, {"Dan": "fellow",
                                            "Simon": "staff"})

        amity_rooms = dict()
        for room in rooms:
            amity_rooms[room.room_name] = room.room_type

        self.assertDictEqual(amity_rooms, {"Riverwood": "office",
                                           "Java": "livingspace"})

        amity_rooms = set()
        amity_people = set()
        for allocation in allocated:
            amity_rooms.add(allocation.room_name)
            amity_people.add(allocation.person_name)

        self.assertSetEqual(amity_people, {"Dan", "Simon"})
        self.assertSetEqual(amity_rooms, {"Riverwood", "Java"})

    def test_loads_state(self):
        # Add data to test_database and check if added
        data = list()
        data.append(People(person_name="Brian", person_type="fellows",
                           wants_accommodation=True))
        data.append(People(person_name="Garfield", person_type="staff"))
        data.append(Rooms(room_name="America", room_type="offices"))
        data.append(Rooms(room_name="Java", room_type="livingspaces"))
        data.append(Allocations(room_name="America", person_name="Garfield"))
        data.append(Allocations(room_name="America", person_name="Brian"))
        self.session.bulk_save_objects(data)
        self.session.commit()

        self.amity.load_amity("test_database")

        assert self.amity.total_no_of_rooms == 2
        assert self.amity.total_no_of_people == 2

    def test_does_not_create_database_with_reserved_name(self):
        self.amity.save_amity("some_database")
        db_path = os.path.dirname(
            os.path.realpath(__file__)) + "/../"

        db_complete_name = os.path.join(db_path, "some_database.db")

        assert not os.path.isfile(db_complete_name)


if __name__ == "__main__":
    unittest.main()
