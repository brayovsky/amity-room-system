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
        self.allocated_rooms = {}

    def add_room(self, room_names, room_type):
        """Adds rooms into amity"""

        set_of_new_rooms = set(room_names)

        # Ensure there are no duplicates
        if room_type == "offices":
            opposite_room = "livingspaces"
        else:
            opposite_room = "offices"

        new_set = set_of_new_rooms.union(self.rooms[opposite_room])
        expected_length = len(self.rooms[opposite_room]) + len(set_of_new_rooms)

        if len(new_set) < expected_length:
            # Duplicate exists
            print("There are rooms that already exist. Please try again with new names")
            return

        # Add new rooms
        self.rooms[room_type] = self.rooms[room_type].union(set_of_new_rooms)
        print("Rooms added succesfully")
        self.total_no_of_rooms = len(self.rooms["offices"]) + len(self.rooms["livingspaces"])
        self.print_allocations()

    def add_person(self, person_name, person_type, wants_accommodation=False):
        """Adds a person into amity"""

        # Staff should not have accommodation
        if person_type == "staff" and wants_accommodation:
            print("Staff cannot have accommodation")

        person = {person_name, }
        self.people[person_type] = self.people[person_type].union(person)
        self.total_no_of_people = len(self.people["fellows"]) + len(self.people["staff"])


    def load_people(self, filename):
        pass

    def print_allocations(self, filename=None):
        print(self.rooms)
        print(self.people)
        print("Total number of people is {0}".format(self.total_no_of_people))
        print("Total number of rooms is {0}".format(self.total_no_of_rooms))


    def print_unallocated(self, filename=None):
        pass

    def save_amity(self, db_name):
        pass

    def load_amity(self, db_name):
        pass