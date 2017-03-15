class Room:
    def __init__(self, amity, room_name):
        pass

    def assign_occupant(self, person_name):
        pass

    def evacuate_occupant(self, person_name):
        pass

    def show_all_occupants(self, person_name):
        pass


class Office(Room):
    def __init__(self, amity, room_name):
        super(Office, self).__init__(amity, room_name)
        self.max_no_of_occupants = 6


class LivingSpace(Room):
    def __init__(self, amity, room_name):
        super(LivingSpace, self).__init__(amity, room_name)
        self.max_no_of_occupants = 4
