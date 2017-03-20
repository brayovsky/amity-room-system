from Person import Fellow, Staff
import os


class Amity:
    def __init__(self):
        self.total_no_of_rooms = 0
        self.total_no_of_people = 0
        self.rooms = {"offices": set(),
                      "livingspaces": set()
                      }
        self.people = {"fellows": set(),
                       "staff": set()
                       }
        self.unbooked_people = {"offices": set(),
                                "livingspaces": set()
                                }
        self.allocations = {"offices": {},
                            "livingspaces": {}
                            }

    def add_room(self, room_names, room_type):
        """Adds rooms into amity"""

        # Capitalize all room names
        room_names = [room_name.capitalize() for room_name in room_names]
        set_of_new_rooms = set(room_names)

        new_set_length = len(set_of_new_rooms | self.rooms["offices"] | self.rooms["livingspaces"])
        expected_length = len(self.rooms["offices"]) + len(self.rooms["livingspaces"]) + len(set_of_new_rooms)

        if new_set_length < expected_length:
            # Duplicate exists
            print("There are rooms that already exist. Duplicate rooms will be removed. The duplicates are:")

            # Get duplicates and remove them from set_of_new_rooms
            all_rooms = self.rooms["livingspaces"] | self.rooms["offices"]
            duplicate_rooms = set_of_new_rooms & all_rooms

            for duplicate_room in duplicate_rooms:
                print(duplicate_room)
                set_of_new_rooms.discard(duplicate_room)

        # Add new rooms
        self.rooms[room_type] |= set_of_new_rooms
        # Add new rooms to allocations
        for room in set_of_new_rooms:
            self.allocations[room_type][room] = set()
        print("Rooms added succesfully")
        self.total_no_of_rooms = len(self.rooms["offices"]) + len(self.rooms["livingspaces"])
        self.show_state()

    def add_person(self, person_name, person_type, wants_accommodation=False):
        """Adds a person into amity"""

        person_name = person_name.capitalize()
        person = {person_name, }

        # Check for duplicates in other peron types
        if person_type == "fellows":
            opposite_person_type = "staff"
        elif person_type == "staff":
            opposite_person_type = "fellows"

        new_set = self.people[opposite_person_type] | person
        expected_length = len(self.people[opposite_person_type]) + 1

        if len(new_set) < expected_length:
            print("{} Already exists. He/She cannot be re-added.".format(person_name))
            return

        # Staff should not have accommodation
        if person_type == "staff" and wants_accommodation:
            print("Staff cannot have accommodation")

        self.people[person_type] |= person
        self.unbooked_people["offices"].add(person_name)

        if person_type == "fellows" and wants_accommodation:
            self.unbooked_people["livingspaces"].add(person_name)

        self.total_no_of_people = len(self.people["fellows"]) + len(self.people["staff"])

        self.show_state()

    def load_people(self, person):
        """Loads people from a text file into amity.
           A sample line of the file is:
           FIRSTNAME LASTNAME FELLOW|STAFF Y
        """
        person = person.split()

        # Combine first and last names
        try:
            person[0] += " " + person.pop(1)
        except IndexError:
            print("Please use a valid file format.")
            return

        if len(person) < 2 or len(person) > 3:
            print("Wrong format encountered. Please check the line at '{}'. \
                   Use the format FIRSTNAME LASTNAME FELLOW|STAFF Y".format(person[0]))
            return

        if person[1] != "STAFF" and person[1] != "FELLOW":
            # wrong format
            print("Wrong format encountered. Please check the line at '{}. \
                  The third word should be STAFF or FELLOW".format(person[0]))
            return

        if len(person) == 3 and person[2] != "Y":
            print("Wrong format encountered. Please check the line at '{}'. \
            The fourth word should be Y or none at all".format(person[0]))
            return

        wants_accommodation = False
        if len(person) == 3:
            wants_accommodation = True

        if person[1] == "STAFF":
            self.add_person(person[0], "staff", wants_accommodation)
        elif person[1] == "FELLOW":
            self.add_person(person[0], "fellows", wants_accommodation)

    def allocate(self):
        """Allocates everyone who does not have a room if rooms are available"""
        if self.total_no_of_rooms == 0:
            print("There are no rooms to allocate people to. Create rooms using the command 'create_room'")
            return

        if self.total_no_of_people == 0:
            print("There are no people to allocate rooms to. Add people using the command 'add_person'")
            return

        office_pop_list = set()
        living_space_pop_list = set()
        for person in self.unbooked_people["offices"]:
            # Determine if person is staff or fellow
            if len(set([person]) & self.people["staff"]) > 0:
                staff = Staff(person)
                staff.book_office(self.allocations["offices"])
                if staff.added:
                    office_pop_list.add(staff.name)

                if staff.alarm:
                    break

            elif len(set([person]) & self.people["fellows"]) > 0:
                fellow = Fellow(person)
                fellow.book_office(self.allocations["offices"])
                if fellow.added:
                    office_pop_list.add(fellow.name)

                if fellow.alarm:
                    break

        self.unbooked_people["offices"] -= office_pop_list

        for person in self.unbooked_people["livingspaces"]:
            fellow = Fellow(person)
            fellow.book_living_space(self.allocations["livingspaces"])
            if fellow.added:
                living_space_pop_list.add(fellow.name)

            if fellow.alarm:
                break

        self.unbooked_people["livingspaces"] -= living_space_pop_list

        print(self.allocations)

    def print_allocations(self, filename=None):
        """Shows all room allocations"""
        allocations = "Offices\r\n"
        for office, people in self.allocations["offices"].items():
            allocations += office + "\r\n" + "-"*100 + "\r\n" + ", ".join(people) + "\r\n"*2

        allocations += "\r\nLiving Spaces\r\n"
        for livingspace, people in self.allocations["livingspaces"].items():
            allocations += livingspace + "\r\n" + "-"*100 + "\r\n" + ", ".join(people) + "\r\n"*2
        print(allocations)

        if filename:
            self.save_to_file(filename, allocations)

    def print_unallocated(self, filename=None):
        """Shows all unallocated people"""
        unallocations = "Offices\r\n"
        for people in self.unbooked_people["offices"]:
            unallocations += people + "\r\n"

        unallocations += "\r\nLiving Spaces\r\n"
        for people in self.unbooked_people["livingspaces"]:
            unallocations += people + "\r\n"
        print(unallocations)

        if filename:
            self.save_to_file(filename, unallocations)

    def print_room(self, room_name):
        # ascertain whether room is in amity and is office or livingspace
        room_name = room_name.capitalize()
        room_set = {room_name, }
        if len(self.rooms["offices"] & room_set) > 0:
            room_type = "offices"
        elif len(self.rooms["livingspaces"] & room_set) > 0:
            room_type = "livingspaces"
        else:
            print("{} does not exist in Amity. Create a room using the command 'create_room'".format(room_name))
            return

        print("\n{}\n{}\n{}\n".format(room_name,
                                      "_"*100,
                                      ", ".join(self.allocations[room_type][room_name])
                                      )
              )

    def save_amity(self, db_name):
        pass

    def load_amity(self, db_name):
        pass

    @staticmethod
    def save_to_file(filename, data):
        filename += ".txt"
        save_path = os.path.dirname(os.path.realpath(__file__)) + "/userdata/"
        complete_name = os.path.join(save_path, filename)

        if os.path.isfile(complete_name):
            print("Please use a file that does not exist in the directory to avoid overwriting your files")
            return
        try:
            allocations_file = open(complete_name, "w+")
        except FileNotFoundError:
            print("Please use a filename as opposed to a directory name")
            return

        allocations_file.write(data)
        allocations_file.close()
        print("Data saved to {}".format(complete_name))

    def show_state(self):
        print("--------------------------------------------------")
        print("All rooms in amity")
        print("--------------------------------------------------")
        print(self.rooms)
        print("--------------------------------------------------")
        print("All people in Amity")
        print("--------------------------------------------------")
        print(self.people)
        print("--------------------------------------------------")
        print("People to be allocated")
        print("--------------------------------------------------")
        print(self.unbooked_people)
        print("--------------------------------------------------")
        print("Allocations are")
        print("--------------------------------------------------")
        print(self.allocations)
        print("--------------------------------------------------")
        print("Total number of people is {0}".format(self.total_no_of_people))
        print("--------------------------------------------------")
        print("Total number of rooms is {0}".format(self.total_no_of_rooms))
        print("--------------------------------------------------")