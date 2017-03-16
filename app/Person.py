from Rooms import Office, LivingSpace


class Person:
    def __init__(self, person_name):
        self.name = person_name
        self.added = False
        self.alarm = False

    def book_office(self, allocations):
        self.added = False
        office = Office()
        for office_name, people in allocations.items():
            if len(people) < office.max_no_of_occupants:
                people.add(self.name)
                self.added = True
                return

        self.alarm = True
        print("You have run out of office space. Some people have not been allocated. \
              Create rooms using the command 'create_room'")

    def change_room(self, new_room, amity):
        # conditions
        # person must be valid
        # check if he exists in people
        new_room = new_room.capitalize()
        all_people = amity.people["fellows"] | amity.people["staff"]
        person = {self.name.capitalize(), }
        if len(person & all_people) < 1:
            print("{} does not exist in Amity. Add him using the command 'add_person'".format(self.name))
            return
        # room must be valid
        offices = amity.rooms["offices"]
        livingspaces = amity.rooms["livingspaces"]

        room = {new_room, }
        if len(room & offices) > 0:
            room_type = "offices"
            room_properties = Office()
        elif len(room & livingspaces) > 0:
            room_type = "livingspaces"
            room_properties = LivingSpace()
        else:
            print("{} does not exist in Amity. Add rooms using the command 'create_room'".format(new_room))
            return

        # staff cannot reallocate to livingspaces
        if room_type == "livingspaces" and len(person & amity.people["staff"]) > 0:
            print("Staff cannot be allocated to living spaces")
            return
        # room must have at least one vacant position
        # get room in allocations and if vacant position add, remove person from previous allocations
        if len(amity.allocations[room_type][new_room]) == room_properties.max_no_of_occupants:
            print("{0} cannot be moved to {1} because it is filled to its maximum capacity."
                  .format(self.name.capitalize(), new_room))
            return

        # allocate person the room
        # check if person in unbooked
        try:
            print("Removing from unbooked")
            amity.unbooked_people[room_type].remove(self.name.capitalize())
        except KeyError:
            # remove from allocations
            print("Changing from allocations")
            # need to know previous room
            for amity_room, people in amity.allocations[room_type].items():
                if len(person & people) > 0:
                    people.remove(self.name.capitalize())
                    break

        # add person to new room
        amity.allocations[room_type][new_room].add(self.name.capitalize())


class Staff(Person):
    def __init__(self, person_name):
        super(Staff, self).__init__(person_name)
        pass


class Fellow(Person):
    def __init__(self, person_name):
        super(Fellow, self).__init__(person_name)

    def book_living_space(self, allocations):
        self.added = False
        livingspace = LivingSpace()
        for livingspace_name, people in allocations.items():
            if len(people) < livingspace.max_no_of_occupants:
                people.add(self.name)
                self.added = True
                return

        self.alarm = True
        print("You have run out of living space. Some people have not been allocated. \
                      Create rooms using the command 'create_room'")
