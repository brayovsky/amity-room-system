class Room:
    def __init__(self, room_name):
        self.name = room_name
        self.occupants = set()

    def show_occupants(self):
        """Report occupants of this particular room"""
        if self.occupants:
            return self.name + "\r\n" + "-"*100 + "\r\n" + \
                                   ", ".join(self.occupants) + "\r\n"*2
        else:
            return self.name + "\r\n" + "-"*100 + "\r\n" + \
                                   self.name + " has no occupants" + "\r\n"*2


class Office(Room):
    max_no_of_occupants = 6


class LivingSpace(Room):
    max_no_of_occupants = 4
