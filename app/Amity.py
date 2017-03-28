import random
import os

import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session

from app.Person import Fellow, Staff
from app.Rooms import Office, LivingSpace
from app.settings import *
from app.Model import People, Rooms, Allocations, Base


class Amity:
    total_no_of_rooms = 0
    total_no_of_people = 0
    total_no_of_offices = 0
    total_no_of_livingspaces = 0
    rooms = {}
    people = {}

    def add_room(self, room_names, room_type):
        """Adds rooms into amity"""

        # Capitalize all room names
        room_names = set(room_names)

        # go through rooms adding each
        for room in room_names:
            room = room.capitalize()
            if room not in self.rooms.keys():
                if room_type is "offices":
                    self.rooms[room] = Office(room)
                    print("{} successfully added to Amity".format(room))
                    self.total_no_of_offices += 1
                else:
                    self.rooms[room] = LivingSpace(room)
                    print("{} successfully added to Amity".format(room))
                    self.total_no_of_livingspaces += 1
            else:
                print("{} not added to amity as it already exists in Amity".
                      format(room))

        self.total_no_of_rooms = len(self.rooms)
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
        if person_type is "staff" and wants_accommodation:
            print("{} will be added but cannot be accommodated as"
                  " s/he is a staff member".format(person_name))
            wants_accommodation = False

        # Add the person
        if person_type is "fellows":
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
        office_reason = None

        perused_offices = set()
        is_assigned_office = False
        assign_office = True

        if not self.total_no_of_offices:
            office_reason = "You have run out of offices"

        if self.people[person_name].office:
            # Has been assigned an office.
            is_assigned_office = False
            assign_office = False
            office_reason = "{} already has an office".format(person_name)

        while assign_office and self.total_no_of_offices:
            try:
                amity_room = random.choice(rooms)
                if type(amity_room) is LivingSpace:
                    continue
            except IndexError:
                break
            if amity_room not in perused_offices and \
               type(amity_room) is Office and \
               len(amity_room.occupants) < amity_room.max_no_of_occupants:
                amity_room.occupants.add(person_name)
                self.people[person_name].office = amity_room.name
                is_assigned_office = True
                assign_office = False
            perused_offices.add(amity_room)
            if len(perused_offices) is self.total_no_of_offices:
                office_reason = "You have run out of offices"
                break

        if wants_accommodation:
            livingspace_info = self.assign_random_livingspace(person_name,
                                                              rooms)
            is_assigned_accommodation = livingspace_info["assigned"]
            livingspace_reason = livingspace_info["reason"]
        else:
            is_assigned_accommodation = False
            livingspace_reason = "{} does not want accommodation". \
                format(person_name)

        return {"office": {"assigned": is_assigned_office,
                           "reason": office_reason},
                "livingspace": {"assigned": is_assigned_accommodation,
                                "reason": livingspace_reason}}

    def assign_random_livingspace(self, person_name, rooms):
        livingspace_reason = None
        is_assigned_accommodation = False
        assign_accommodation = True
        perused_livingspaces = set()
        if self.people[person_name].livingspace:
            # Has been assigned a livingspace.
            is_assigned_accommodation = False
            assign_accommodation = False
            livingspace_reason = "{} already has a livingspace". \
                format(person_name)

        if not self.total_no_of_livingspaces:
            livingspace_reason = "You have run out of livingspaces"

        while assign_accommodation and self.total_no_of_livingspaces:
            try:
                amity_room = random.choice(rooms)
                if type(amity_room) is Office:
                    continue
            except IndexError:
                break
            if amity_room not in perused_livingspaces and \
               type(amity_room) is LivingSpace and \
               len(amity_room.occupants) < amity_room.max_no_of_occupants:

                amity_room.occupants.add(person_name)
                self.people[person_name].livingspace = amity_room.name
                is_assigned_accommodation = True
                assign_accommodation = False
            perused_livingspaces.add(amity_room)
            if len(perused_livingspaces) is self.total_no_of_livingspaces:
                livingspace_reason = "You have run out of livingspaces"
                break

        return {"assigned": is_assigned_accommodation,
                "reason": livingspace_reason}

    def reallocate_person(self, person_name, new_room):
        person_name = person_name.capitalize()
        new_room = new_room.capitalize()

        if person_name not in self.people.keys():
            print("{} does not exist in amity".format(person_name))
            return

        if type(self.rooms[new_room]) is LivingSpace and \
           type(self.people[person_name]) is Staff:
            print("Staff cannot be reallocated to livingspaces")
            return

        if type(self.rooms[new_room]) is LivingSpace and not \
           self.people[person_name].wants_accommodation:
            print("{} does not want accommodation".format(person_name))
            return

        person = self.people[person_name]
        room = self.rooms[new_room]

        if type(room) is Office:
            assignment = person.change_office(new_room, self.rooms)
        else:
            assignment = person.change_livingspace(new_room, self.rooms)

        if assignment:
            print("{} successfully moved to {}".format(person_name, new_room))
        else:
            print("{} could not be moved to {}".format(person_name, new_room))

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
                   Use the format FIRSTNAME LASTNAME FELLOW|STAFF Y".
                  format(person[0]))
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
            if type(person) is Fellow:
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
                if type(room) is Office:
                    allocations += room.show_occupants()
        else:
            allocations += "There are no offices that have been added to Amity"

        allocations += "\r\nLiving Spaces\r\n"
        if self.total_no_of_livingspaces:
            for room_name, room in self.rooms.items():
                if type(room) is LivingSpace:
                    allocations += room.show_occupants()
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

        if unallocations is "Offices\r\n":
            unallocations += "Everyone has been placed in an office"

        unallocations += "\r\nLiving Spaces\r\n"
        for person_name, person in self.people.items():
            if type(person) is Fellow and person.wants_accommodation \
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
            amity = list()
            for person in self.people.values():
                if person.office:
                    amity.append(Allocations(person_name=person.name,
                                             room_name=person.office))
                if type(person) is Fellow:
                    amity.append(People(person_name=person.name,
                                        person_type="fellow",
                                        wants_accommodation=person.
                                        wants_accommodation))
                    if person.livingspace:
                        amity.append(Allocations(person_name=person.name,
                                                 room_name=person.livingspace))
                else:
                    amity.append(People(person_name=person.name,
                                        person_type="staff"))

            for room in self.rooms.values():
                if type(room) is Office:
                    amity.append(Rooms(room_name=room.name,
                                       room_type="office"))
                else:
                    amity.append(Rooms(room_name=room.name,
                                       room_type="livingspace"))

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
            if not session:
                return

            # Clear data
            self.clear_amity_data()
            all_people = session.query(People)
            all_rooms = session.query(Rooms)
            allocations = session.query(Allocations)
            for person in all_people:
                if person.person_type is "staff":
                    self.people[person.person_name] = \
                        Staff(person.person_name)
                else:
                    self.people[person.person_name] = \
                        Fellow(person.person_name,
                               wants_accommodation=person.wants_accommodation)

            for room in all_rooms:
                if room.room_type is "office":
                    self.rooms[room.room_name] = Office(room.room_name)
                else:
                    self.rooms[room.room_name] = \
                        LivingSpace(room.room_name)

            for allocation in allocations:
                if type(self.rooms[allocation.room_name]) is Office:
                    self.people[allocation.person_name].office = \
                        allocation.room_name
                    self.rooms[allocation.room_name].occupants.\
                        add(allocation.person_name)
                    self.total_no_of_offices += 1
                else:
                    self.people[allocation.person_name].livingspace = \
                        allocation.room_name
                    self.rooms[allocation.room_name].occupants. \
                        add(allocation.person_name)
                    self.total_no_of_livingspaces += 1

            self.total_no_of_rooms = len(self.rooms)
            self.total_no_of_people = len(self.people)

            print("Data from {} has been loaded.".format(db_name))

        except sqlalchemy.exc.OperationalError:
            print("Incompatible database format. "
                  "Please use a database created by amity system")

    def clear_amity_data(self):
        self.total_no_of_rooms = 0
        self.total_no_of_people = 0
        self.total_no_of_offices = 0
        self.total_no_of_livingspaces = 0
        self.rooms = {}
        self.people = {}

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
            print("Please use a file that does not exist in the directory"
                  " to avoid overwriting your files.")
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
