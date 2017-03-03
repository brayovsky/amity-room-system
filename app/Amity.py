class Amity:
    def __init__(self):
        self.total_no_of_rooms = 0
        self.total_no_of_people = 0
        self.rooms = {}
        self.people = {}
        self.allocated_rooms = {}
        self.unallocated_people = {}

    def add_room(self, room_name, room_type):
        pass

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