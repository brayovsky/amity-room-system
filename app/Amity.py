from app.Person import Fellow, Staff
from app.Rooms import Office, LivingSpace
from app.settings import *
import random
import os
from app.Model import People, Rooms, Allocations, Base
import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session


class Amity:
    total_no_of_rooms = 0
    total_no_of_people = 0
    total_no_of_offices = 0
    total_no_of_livingspaces = 0
    rooms = {}
    people = {}
    unbooked_people = {"offices": set(),
                       "livingspaces": set()
                        }

    def add_room(self, room_names, room_type):
        """Adds rooms into amity"""

        # Capitalize all room names
        room_names = set(room_names)

        # go through rooms adding each
        for room in room_names:
            room = room.capitalize()
            if room not in self.rooms:
                if room_type == "offices":
                    self.rooms[room] = Office(room)
                    print("{} successfully added to Amity".format(room))
                    self.total_no_of_offices += 1
                else:
                    self.rooms[room] = LivingSpace(room)
                    print("{} successfully added to Amity".format(room))
                    self.total_no_of_livingspaces += 1
                self.total_no_of_rooms += 1
            else:
                print("{} not added to amity as it already exists in Amity".
                      format(room))

        self.show_state()

    def add_person(self, person_name, person_type, wants_accommodation=False):
        """Adds a person into amity"""

        person_name = person_name.capitalize()

        # Check for duplicates
        if person_name in self.people:
            print("{} already exists in amity and cannot be re-added".
                  format(person_name))
            return

        # Staff should not have accommodation
        if person_type == "staff" and wants_accommodation:
            print("{} will be added but cannot be accomodated as he is a staff"
                  " member".format(person_name))
            wants_accommodation = False

        # Add the person
        if person_type == "fellows":
            self.people[person_name] = Fellow(person_name, wants_accommodation)
        else:
            self.people[person_name] = Staff(person_name)
        self.total_no_of_people += 1

        # Assign room
        allocation = self.assign_random_room(person_name, wants_accommodation)

        if allocation["office"]["assigned"]:
            print("{} has been added and assigned the office {}".
                  format(person_name, self.people[person_name].office))
        elif not allocation["office"]["assigned"]:
            print("{} has been added but has not been assigned an office".
                  format(person_name))

        if not wants_accommodation:
            self.show_state()
            return

        if allocation["livingspace"]["assigned"]:
            print("{} has been assigned the livingspace {}".
                  format(person_name, self.people[person_name].livingspace))
        elif not allocation["livingspace"]["assigned"]:
            print("{} has not been assigned a livingspace".format(person_name))

        self.show_state()

    def assign_random_room(self, person_name, wants_accommodation):
        """Assigns a random room to a person"""
        rooms = list(self.rooms.values())
        livingspace_reason = None
        office_reason = None

        perused_offices = set()
        is_assigned_office = False
        assign_office = True

        if not self.total_no_of_offices:
            office_reason = "You have run out of offices"

        if self.people[person_name].office:
            # has been assigned an office
            is_assigned_office = False
            assign_office = False
            office_reason = "{} already has an office".format(person_name)

        while assign_office and self.total_no_of_offices:
            try:
                amity_room = random.choice(rooms)
                if type(amity_room) == LivingSpace:
                    continue
            except IndexError:
                break
            if amity_room not in perused_offices and \
               type(amity_room) == Office and \
               len(amity_room.occupants) < amity_room.max_no_of_occupants:
                amity_room.occupants.add(person_name)
                self.people[person_name].office = amity_room.name
                is_assigned_office = True
                assign_office = False
            perused_offices.add(amity_room)
            if len(perused_offices) == self.total_no_of_offices:
                office_reason = "You have run out of offices"
                break

        is_assigned_accommodation = False
        assign_accommodation = True
        perused_livingspaces = set()
        if wants_accommodation:
            if self.people[person_name].livingspace:
                # has been assigned a livingspace
                is_assigned_accommodation = False
                assign_accommodation = False
                livingspace_reason = "{} already has a livingspace".\
                    format(person_name)
            if not self.total_no_of_livingspaces:
                livingspace_reason = "You have run out of livingspaces"
            while assign_accommodation and self.total_no_of_livingspaces:
                try:
                    amity_room = random.choice(rooms)
                    if type(amity_room) == Office:
                        continue
                except IndexError:
                    break
                if amity_room not in perused_livingspaces and \
                   type(amity_room) == LivingSpace and \
                   len(amity_room.occupants) < amity_room.max_no_of_occupants:
                    amity_room.occupants.add(person_name)
                    self.people[person_name].livingspace = amity_room.name
                    is_assigned_accommodation = True
                    assign_accommodation = False
                perused_livingspaces.add(amity_room)
                if len(perused_livingspaces) == self.total_no_of_livingspaces:
                    livingspace_reason = "You have run out of livingspaces"
                    break
        else:
            livingspace_reason = "{} does not want accommodation". \
                format(person_name)

        return {"office": {"assigned": is_assigned_office,
                           "reason": office_reason},
                "livingspace": {"assigned": is_assigned_accommodation,
                                "reason": livingspace_reason}}

    def load_people(self, person_line):
        """Loads people from a text file into amity.
           A sample line of the file is:
           FIRSTNAME LASTNAME FELLOW|STAFF Y
        """
        person = person_line.split()

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
            print("Wrong format encountered. Please check the line at '{}'. "
                  "The fourth word should be Y or none at all".
                  format(person[0]))
            return

        wants_accommodation = False
        if len(person) == 3:
            wants_accommodation = True

        if person[1] == "STAFF":
            self.add_person(person[0], "staff", wants_accommodation)
        elif person[1] == "FELLOW":
            self.add_person(person[0], "fellows", wants_accommodation)

        self.show_state()

    def allocate(self):
        """Allocates everyone who does not have
        a room if rooms are available"""
        if self.total_no_of_rooms == 0:
            print("There are no rooms to allocate people to."
                  "Create rooms using the command 'create_room'")
            return False

        if self.total_no_of_people == 0:
            print("There are no people to allocate rooms to."
                  " Add people using the command 'add_person'")
            return False

        # Check if person already allocated
        # Return reason for not allocating from assign_random_room()
        for person_name, person in self.people.items():
            if type(person) == Fellow:
                is_fellow = True
                allocation = \
                    self.assign_random_room(person.name,
                                            person.wants_accommodation)
            else:
                is_fellow = False
                allocation = \
                    self.assign_random_room(person.name,
                                            wants_accommodation=False)

            if allocation["office"]["assigned"]:
                print("{} has been assigned the office {}".
                      format(person.name, person.office))
            elif not allocation["office"]["assigned"]:
                print("{} has been not been assigned an office. {}"
                      .format(person.name,
                              allocation["office"]["reason"]))

            if allocation["livingspace"]["assigned"] and is_fellow:
                print("{} has been assigned the livingspace {}".
                      format(person.name, person.livingspace))
            elif not allocation["livingspace"]["assigned"] and is_fellow:
                print("{} has been not been assigned a livingspace {}".
                      format(person.name,
                             allocation["livingspace"]["reason"]))

        self.show_state()

    def print_allocations(self, filename=None):
        """Shows all room allocations"""
        allocations = "Offices\r\n"
        if self.total_no_of_offices:
            for room_name, room in self.rooms.items():
                if type(room) == Office and room.occupants:
                    allocations += room.name + "\r\n" + "-"*100 + "\r\n" + \
                                   ", ".join(room.occupants) + "\r\n"*2
                elif type(room) == Office and not room.occupants:
                    allocations += room.name + "\r\n" + "-"*100 + "\r\n" + \
                                   room.name + " has no occupants" + "\r\n"*2
        else:
            allocations += "There are no offices that have been added to Amity"

        allocations += "\r\nLiving Spaces\r\n"
        if self.total_no_of_livingspaces:
            for room_name, room in self.rooms.items():
                if type(room) == LivingSpace and room.occupants:
                    allocations += room.name + "\r\n" + "-"*100 + "\r\n" + \
                                   ", ".join(room.occupants) + "\r\n"*2
                elif type(room) == LivingSpace and not room.occupants:
                    allocations += room.name + "\r\n" + "-" * 100 + "\r\n" + \
                                   room.name + " has no occupants" + "\r\n" * 2
        else:
            allocations += \
                "There are no livingspaces that have been added to Amity"

        print(allocations)

        if filename and self.save_to_file(filename, allocations):
            print("File complete and saved")

    def print_unallocated(self, filename=None):
        """Shows all unallocated people"""
        if not self.total_no_of_people:
            print("There are no people in Amity. Add people first")
            return

        unallocations = "Offices\r\n"
        for person_name, person in self.people.items():
            if not person.office:
                unallocations += person_name + "\r\n"

        if unallocations == "Offices\r\n":
            unallocations += "Everyone has been placed in an office"

        unallocations += "\r\nLiving Spaces\r\n"
        for person_name, person in self.people.items():
            if type(person) == Fellow and person.wants_accommodation \
                    and not person.livingspace:
                unallocations += person_name + "\r\n"

        if unallocations[-17:] == "\r\nLiving Spaces\r\n":
            unallocations += "Every eligible fellow has been accommodated"

        print(unallocations)

        if filename:
            self.save_to_file(filename, unallocations)

    def print_room(self, room_name):
        # ascertain whether room is in amity and is office or livingspace
        room_name = room_name.capitalize()
        try:
            room = self.rooms[room_name]
            if not room.occupants:
                print("{} has no occupants".format(room.name))
                return
            print("\n{}\n{}\n{}\n".format(room.name,
                                          "_"*100,
                                          ", ".join(room.occupants)
                                          )
                  )
        except KeyError:
            print("{} does not exist in Amity. Create the room first".
                  format(room_name))

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
        if not DEBUG:
            return
        print("Rooms are\n{}".format("-"*65))
        for room_name, amity_room in self.rooms.items():
            print(amity_room.name + "(" + str(type(amity_room)) + ") -> ")
            print(amity_room.occupants)
        print("People are\n{}".format("-"*65))
        for person_name, amity_person in self.people.items():
            print(amity_person.name + " -> ")
            print(amity_person.office)
            try:
                print(amity_person.livingspace)
            except AttributeError:
                pass
