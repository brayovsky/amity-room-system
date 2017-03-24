class Room:
    def __init__(self, room_name):
        self.name = room_name
        self.occupants = set()


class Office(Room):
    max_no_of_occupants = 6


class LivingSpace(Room):
    max_no_of_occupants = 4
