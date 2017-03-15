class Person:
    def __init__(self, person_name):
        self.name = person_name
        self.added = False
        self.alarm = False

    def book_office(self, allocations, unbooked_people):
        print("Booking office for {}".format(self.name))
        # Take first office and add, if full, go to next
        print(allocations)
        self.added = False
        for office, people in allocations.items():
            if len(people) < 6:
                people.add(self.name)
                self.added = True
                return

        self.alarm = True
        print("You have run out of office space. Some people have not been allocated. \
              Create rooms using the command 'create_room'")

        """
        Books a person into an office
        :param office_name: Office to book into
        :return:
        """

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
