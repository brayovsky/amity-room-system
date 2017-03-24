from app.Person import Fellow, Staff
import os
from app.Model import People, Rooms, Allocations, Base
import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session


class Amity:
    def __init__(self):
        self.total_no_of_rooms = 0
        self.total_no_of_people = 0
        self.rooms = {"offices": set(),
                      "livingspaces": set()
                      }
        self.people = {"fellows": set(),
                       "staff": set()
                       }
        self.unbooked_people = {"offices": set(),
                                "livingspaces": set()
                                }
        self.allocations = {"offices": {},
                            "livingspaces": {}
                            }

    def add_room(self, room_names, room_type):
        """Adds rooms into amity"""

        # Capitalize all room names
        room_names = [room_name.capitalize() for room_name in room_names]
        set_of_new_rooms = set(room_names)

        new_set_length = len(set_of_new_rooms | self.rooms["offices"] | self.rooms["livingspaces"])
        expected_length = len(self.rooms["offices"]) + len(self.rooms["livingspaces"]) + len(set_of_new_rooms)

        if new_set_length < expected_length:
            # Duplicate exists
            print("There are rooms that already exist. Duplicate rooms will be removed. The duplicates are:")

            # Get duplicates and remove them from set_of_new_rooms
            all_rooms = self.rooms["livingspaces"] | self.rooms["offices"]
            duplicate_rooms = set_of_new_rooms & all_rooms

            for duplicate_room in duplicate_rooms:
                print(duplicate_room)
                set_of_new_rooms.discard(duplicate_room)

        # Add new rooms
        self.rooms[room_type] |= set_of_new_rooms
        # Add new rooms to allocations
        for room in set_of_new_rooms:
            print("{} added succesfully".format(room))
            self.allocations[room_type][room] = set()

        self.total_no_of_rooms = len(self.rooms["offices"]) + len(self.rooms["livingspaces"])
        # self.show_state()

    def add_person(self, person_name, person_type, wants_accommodation=False):
        """Adds a person into amity"""

        person_name = person_name.capitalize()
        person = {person_name, }

        # Check for duplicates in other peron types
        if person_type == "fellows":
            opposite_person_type = "staff"
        elif person_type == "staff":
            opposite_person_type = "fellows"

        new_set = self.people[opposite_person_type] | person
        expected_length = len(self.people[opposite_person_type]) + 1

        if len(new_set) < expected_length:
            print("{} Already exists. He/She cannot be re-added.".format(person_name))
            return

        # Staff should not have accommodation
        if person_type == "staff" and wants_accommodation:
            print("Staff cannot have accommodation")

        self.people[person_type] |= person
        self.unbooked_people["offices"].add(person_name)

        if person_type == "fellows" and wants_accommodation:
            self.unbooked_people["livingspaces"].add(person_name)

        self.total_no_of_people = len(self.people["fellows"]) + len(self.people["staff"])
        # self.show_state()

    def load_people(self, person):
        """Loads people from a text file into amity.
           A sample line of the file is:
           FIRSTNAME LASTNAME FELLOW|STAFF Y
        """
        person = person.split()

        # Combine first and last names
        try:
            person[0] += " " + person.pop(1)
        except IndexError:
            print("Please use a valid file format.")
            return

        if len(person) < 2 or len(person) > 3:
            print("Wrong format encountered. Please check the line at '{}'. \
                   Use the format FIRSTNAME LASTNAME FELLOW|STAFF Y".format(person[0]))
            return

        if person[1] != "STAFF" and person[1] != "FELLOW":
            # wrong format
            print("Wrong format encountered. Please check the line at '{}. \
                  The third word should be STAFF or FELLOW".format(person[0]))
            return

        if len(person) == 3 and person[2] != "Y":
            print("Wrong format encountered. Please check the line at '{}'. \
            The fourth word should be Y or none at all".format(person[0]))
            return

        wants_accommodation = False
        if len(person) == 3:
            wants_accommodation = True

        if person[1] == "STAFF":
            self.add_person(person[0], "staff", wants_accommodation)
        elif person[1] == "FELLOW":
            self.add_person(person[0], "fellows", wants_accommodation)

    def allocate(self):
        """Allocates everyone who does not have a room if rooms are available"""
        if self.total_no_of_rooms == 0:
            print("There are no rooms to allocate people to. Create rooms using the command 'create_room'")
            return False

        if self.total_no_of_people == 0:
            print("There are no people to allocate rooms to. Add people using the command 'add_person'")
            return False

        office_pop_list = set()
        living_space_pop_list = set()
        for person in self.unbooked_people["offices"]:
            # Determine if person is staff or fellow
            if len(set([person]) & self.people["staff"]) > 0:
                staff = Staff(person)
                staff.book_office(self.allocations["offices"])
                if staff.added:
                    office_pop_list.add(staff.name)

                if staff.alarm:
                    break

            elif len(set([person]) & self.people["fellows"]) > 0:
                fellow = Fellow(person)
                fellow.book_office(self.allocations["offices"])
                if fellow.added:
                    office_pop_list.add(fellow.name)

                if fellow.alarm:
                    break

        self.unbooked_people["offices"] -= office_pop_list

        for person in self.unbooked_people["livingspaces"]:
            fellow = Fellow(person)
            fellow.book_living_space(self.allocations["livingspaces"])
            if fellow.added:
                living_space_pop_list.add(fellow.name)

            if fellow.alarm:
                break

        self.unbooked_people["livingspaces"] -= living_space_pop_list

    def print_allocations(self, filename=None):
        """Shows all room allocations"""
        allocations = "Offices\r\n"
        for office, people in self.allocations["offices"].items():
            allocations += office + "\r\n" + "-"*100 + "\r\n" + ", ".join(people) + "\r\n"*2

        allocations += "\r\nLiving Spaces\r\n"
        for livingspace, people in self.allocations["livingspaces"].items():
            allocations += livingspace + "\r\n" + "-"*100 + "\r\n" + ", ".join(people) + "\r\n"*2
        print(allocations)

        if filename and self.save_to_file(filename, allocations):
            print("File complete and saved")

    def print_unallocated(self, filename=None):
        """Shows all unallocated people"""
        unallocations = "Offices\r\n"
        for people in self.unbooked_people["offices"]:
            unallocations += people + "\r\n"

        unallocations += "\r\nLiving Spaces\r\n"
        for people in self.unbooked_people["livingspaces"]:
            unallocations += people + "\r\n"
        print(unallocations)

        if filename:
            self.save_to_file(filename, unallocations)

    def print_room(self, room_name):
        # ascertain whether room is in amity and is office or livingspace
        room_name = room_name.capitalize()
        room_set = {room_name, }
        if len(self.rooms["offices"] & room_set) > 0:
            room_type = "offices"
        elif len(self.rooms["livingspaces"] & room_set) > 0:
            room_type = "livingspaces"
        else:
            print("{} does not exist in Amity. Create a room using the command 'create_room'".format(room_name))
            return

        print("\n{}\n{}\n{}\n".format(room_name,
                                      "_"*100,
                                      ", ".join(self.allocations[room_type][room_name])
                                      )
              )

    def save_amity(self, db_name=None):
        reserved_names = ["test_database", "some_database"]
        if db_name:
            if db_name.lower() in reserved_names:
                print("{} is a reserved database name. Please use another name"
                      .format(db_name))
                return False
            db_name += ".db"
        else:
            db_name = "amity.db"
            
        # check if database exists
        if self.check_db_exists(db_name):
            self.reset_db(db_name)
            self.create_database(db_name)
        else:
            self.create_database(db_name)
        self.save_current_data(db_name)

    def save_current_data(self, db_name):
        session = self.connect_to_db(db_name)

        if not session:
            return

        try:
            amity = []
            for fellow in self.people["fellows"]:
                wants_accommodation = False
                if {fellow, } & self.unbooked_people["livingspaces"]:
                    wants_accommodation = True
                amity.append(People(person_name=fellow, person_type="fellows", wants_accommodation=wants_accommodation))
                
            for staff in self.people["staff"]:
                amity.append(People(person_name=staff, person_type="staff"))
            for office in self.rooms["offices"]:
                amity.append(Rooms(room_name=office, room_type="offices"))
            for livingspace in self.rooms["livingspaces"]:
                amity.append(Rooms(room_name=livingspace, room_type="livingspaces"))
            for office, people in self.allocations["offices"].items():
                for person in people:
                    amity.append(Allocations(room_name=office,
                                             person_name=person
                                             )
                                 )
            for livingspace, people in self.allocations["livingspaces"].items():
                for person in people:
                    amity.append(Allocations(room_name=livingspace,
                                             person_name=person
                                             )
                                 )

            session.bulk_save_objects(amity)
            session.commit()
            print("Data saved to {}".format(db_name))
        except sqlalchemy.exc.IntegrityError:
            print("New data added to database")

    def load_amity(self, db_name):
        # Check if database exists
        db_name += ".db"
        if not self.check_db_exists(db_name):
            print("{} database does not exist.".format(db_name))
            return

        try:
            session = self.connect_to_db(db_name)
            if session:
                # Clear data
                self.clear_amity_data()
                all_people = session.query(People)
                all_rooms = session.query(Rooms)
                allocations = session.query(Allocations)
                for person in all_people:
                    self.people[person.person_type].add(person.person_name)
                    self.total_no_of_people += 1
                for room in all_rooms:
                    self.rooms[room.room_type].add(room.room_name)
                    self.total_no_of_rooms += 1
                    # Add all rooms to allocations
                    self.allocations[room.room_type][room.room_name] = set()

                for allocation in allocations:
                    room_type = session.query(Rooms.room_type).\
                        filter_by(room_name=allocation.room_name).scalar()
                    try:
                        self.allocations[room_type][allocation.room_name].\
                            add(allocation.person_name)
                    except KeyError:
                        self.allocations[room_type][allocation.room_name] = \
                            {allocation.person_name, }

                people_names = self.people["fellows"] | self.people["staff"]
                allocated_people = session.query(Allocations.person_name).distinct()
                allocated_names = set([allocated_person[0] for allocated_person in allocated_people])
                unbooked_people = people_names - allocated_names
                self.unbooked_people["offices"] = unbooked_people

                unaccommodated_fellows = session.query(People.person_name).filter_by(wants_accommodation=True)
                unaccommodated_fellow_names = set([fellow[0] for fellow in unaccommodated_fellows])
                self.unbooked_people["livingspaces"] = unaccommodated_fellow_names

        except sqlalchemy.exc.OperationalError:
            print("Incompatible database format. Please use a database created by amity system")

    def clear_amity_data(self):
        self.total_no_of_rooms = 0
        self.total_no_of_people = 0
        self.rooms = {"offices": set(),
                      "livingspaces": set()
                      }
        self.people = {"fellows": set(),
                       "staff": set()
                       }
        self.unbooked_people = {"offices": set(),
                                "livingspaces": set()
                                }
        self.allocations = {"offices": {},
                            "livingspaces": {}
                            }

    @staticmethod
    def create_database(db_name):
        engine = create_engine("sqlite:///" + db_name)
        Base.metadata.create_all(engine)

    @staticmethod
    def reset_db(db_name):
        engine = create_engine("sqlite:///" + db_name)
        Base.metadata.drop_all(engine)

    @staticmethod
    def connect_to_db(db_name):
        engine = create_engine('sqlite:///' + db_name)
        db_session = sessionmaker(bind=engine)
        session = db_session()
        return session

    @staticmethod
    def save_to_file(filename, data):
        filename += ".txt"
        save_path = os.path.dirname(os.path.realpath(__file__)) + "/userdata/"
        complete_name = os.path.join(save_path, filename)

        if os.path.isfile(complete_name):
            print("Please use a file that does not exist in the directory to avoid overwriting your files")
            return False
        try:
            allocations_file = open(complete_name, "w+")
        except FileNotFoundError:
            print("Please use a filename as opposed to a directory name")
            return False

        allocations_file.write(data)
        allocations_file.close()
        print("Data saved to {}".format(complete_name))
        return True

    @staticmethod
    def check_db_exists(db_name):
        path = os.path.dirname(os.path.realpath(__file__)) + "/../"
        complete_name = os.path.join(path, db_name)

        if os.path.isfile(complete_name):
            return True
        else:
            return False
    def show_state(self):  # pragma: no cover
        print("--------------------------------------------------")
        print("All rooms in amity")
        print("--------------------------------------------------")
        print(self.rooms)
        print("--------------------------------------------------")
        print("All people in Amity")
        print("--------------------------------------------------")
        print(self.people)
        print("--------------------------------------------------")
        print("People to be allocated")
        print("--------------------------------------------------")
        print(self.unbooked_people)
        print("--------------------------------------------------")
        print("Allocations are")
        print("--------------------------------------------------")
        print(self.allocations)
        print("--------------------------------------------------")
        print("Total number of people is {0}".format(self.total_no_of_people))
        print("--------------------------------------------------")
        print("Total number of rooms is {0}".format(self.total_no_of_rooms))
        print("--------------------------------------------------")