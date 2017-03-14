class Amity:
    def __init__(self):
        self.total_no_of_rooms = 0
        self.total_no_of_people = 0
        self.rooms = {"offices": set(),
                      "livingspaces": set()
                      }
        self.people = {"fellows": None,
                       "staff": None
                       }
        self.allocated_rooms = {}

    def add_room(self, room_names, room_type):
        """Adds rooms into amity"""
        set_of_new_rooms = set(room_names)
        self.rooms[room_type] = self.rooms[room_type].union(set_of_new_rooms)
        print("Rooms added succesfully")
        self.total_no_of_rooms += 1
        self.print_allocations()

    def add_person(self, person_name, person_type, wants_accomodation=False):
        pass

    def load_people(self, filename):
        pass

    def print_allocations(self, filename=None):
        pass

    def print_unallocated(self, filename=None):
        pass

    def save_amity(self, db_name):
        pass

    def load_amity(self, db_name):
        pass