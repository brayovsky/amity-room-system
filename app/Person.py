from app.Rooms import Office, LivingSpace


class Person:
    def __init__(self, person_name):
        self.name = person_name
        self.office = None

    def change_office(self, new_room, rooms):
        if new_room not in rooms.keys():
            print("{} does not exist in amity".format(new_room))
            return False

        room = rooms[new_room]

        if type(room) is not Office:
            print("{} must be a livingspace".format(new_room))
            return False

        if len(room.occupants) == room.max_no_of_occupants:
            print("{} is filled".format(new_room))
            return False

        # Remove from previous office and change office
        if self.office:
            rooms[self.office].occupants.discard(self.name)
        room.occupants.add(self.name)
        self.office = new_room

        return True


class Staff(Person):
    pass


class Fellow(Person):
    def __init__(self, person_name, wants_accommodation):
        super(Fellow, self).__init__(person_name)
        self.wants_accommodation = wants_accommodation
        self.livingspace = None

    def change_livingspace(self, new_room, rooms):
        if not self.wants_accommodation:
            return False

        if new_room not in rooms.keys():
            print("{} does not exist in amity".format(new_room))
            return False

        room = rooms[new_room]

        if type(room) is not LivingSpace:
            print("{} must be a livingspace".format(new_room))
            return False

        if len(room.occupants) == room.max_no_of_occupants:
            print("{} is filled".format(new_room))
            return False

        # Remove from previous office and change office
        if self.livingspace:
            rooms[self.livingspace].occupants.discard(self.name)
        room.occupants.add(self.name)
        self.livingspace = new_room

        return True
