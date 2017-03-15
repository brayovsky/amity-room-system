class Person:
    def __init__(self, person_name):
        self.name = person_name

    def book_office(self, allocations, all_rooms):
        print("Booking office for {}".format(self.name))

        """
        Books a person into an office
        :param office_name: Office to book into
        :return:
        """
        pass

    def evacuate_room(self):
        """
        Evacuates a person from a room. Used when changing rooms
        :param room_name: The room to evacuate from
        :return: True or False
        """
        pass

    def change_room(self, old_room, room_type):
        """
        Changes a room
        :param new_room: Room to move from
        :param room_type: Office or livingspace
        :return: True or False
        """
        pass


class Staff(Person):
    def __init__(self, person_name):
        super(Staff, self).__init__(person_name)
        pass


class Fellow(Person):
    def __init__(self, person_name):
        super(Fellow, self).__init__(person_name)
        pass

    def book_living_space(self, allocations, livingspaces):
        """
        Books a fellow into a living space
        :return: True or False
        """
        print("Booking living space for {}".format(self.name))
