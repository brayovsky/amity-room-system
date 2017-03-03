class Person:
    def __init__(self):
        pass

    def book_office(self):
        pass

    def evacuate_room(self):
        pass

    def change_room(self):
        pass


class Staff(Person):
    def __init__(self, amity, person_name):
        super(Staff, self).__init__(amity, person_name)
        pass


class Fellow(Person):
    def __init__(self, amity, person_name):
        super(Fellow, self).__init__(amity, person_name)
        pass

    def book_living_space(self):
        pass