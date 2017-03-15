from Person import Fellow, Staff
from Rooms import Office, LivingSpace

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
                                "livingspaces": set()}
        self.allocations = {"offices": {},
                            "livingspaces": {}}

    def add_room(self, room_names, room_type):
        """Adds rooms into amity"""

        # Capitalize all room names
        room_names = [room_name.capitalize() for room_name in room_names]

        set_of_new_rooms = set(room_names)

        # Ensure there are no duplicates
        if room_type == "offices":
            opposite_room = "livingspaces"
        else:
            opposite_room = "offices"

        new_set = set_of_new_rooms | self.rooms[opposite_room]
        expected_length = len(self.rooms[opposite_room]) + len(set_of_new_rooms)

        if len(new_set) < expected_length:
            # Duplicate exists
            print("There are rooms that already exist. Duplicate rooms will be removed")

            # Get duplicates and remove them from set_of_new_rooms
            all_rooms = self.rooms["livingspaces"] | self.rooms["offices"]
            duplicate_rooms = set_of_new_rooms & all_rooms

            for duplicate_room in duplicate_rooms:
                set_of_new_rooms.discard(duplicate_room)

        # Add new rooms
        self.rooms[room_type] |= set_of_new_rooms
        print("Rooms added succesfully")
        self.total_no_of_rooms = len(self.rooms["offices"]) + len(self.rooms["livingspaces"])
        self.print_allocations()

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

        self.print_allocations()

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
            return

        if self.total_no_of_people == 0:
            print("There are no people to allocate rooms to. Add people using the command 'add_person'")
            return

        # Use person class method to book an office
        # Iterate through unadded people, instantiate their objects and book them
        # Book offices
        for person in self.unbooked_people["offices"]:
            # Determine if person is staff or fellow
            if len(set([person]) & self.people["staff"]) > 0:
                staff = Staff(person)
                staff.book_office(self.allocations["offices"], self.rooms["offices"])
            elif len(set([person]) & self.people["fellows"]) > 0:
                fellow = Fellow(person)
                fellow.book_office(self.allocations["offices"], self.rooms["offices"])

        for person in self.unbooked_people["livingspaces"]:
            fellow = Fellow(person)
            fellow.book_living_space(self.allocations["livingspaces"], self.rooms["livingspaces"])

    def print_allocations(self, filename=None):
        print("--------------------------------------------------")
        print("All rooms in amity")
        print("--------------------------------------------------")
        print(self.rooms)
        print("--------------------------------------------------")
        print("All people in Amity")
        print("--------------------------------------------------")
        print(self.people)
        print("--------------------------------------------------")
        print("Fellows to be accommodated")
        print("--------------------------------------------------")
        print(self.unbooked_people)
        print("--------------------------------------------------")
        print("Total number of people is {0}".format(self.total_no_of_people))
        print("--------------------------------------------------")
        print("Total number of rooms is {0}".format(self.total_no_of_rooms))
        print("--------------------------------------------------")

    def print_unallocated(self, filename=None):
        pass

    def save_amity(self, db_name):
        pass

    def load_amity(self, db_name):
        pass