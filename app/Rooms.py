class Room:
    def __init__(self):
        pass


class Office(Room):
    def __init__(self):
        super(Office, self).__init__()
        self.max_no_of_occupants = 6


class LivingSpace(Room):
    def __init__(self):
        super(LivingSpace, self).__init__()
        self.max_no_of_occupants = 4
