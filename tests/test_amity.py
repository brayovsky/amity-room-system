from unittest import TestCase
import unittest
from tests.basetest import BaseTestCase
import os


class TestAmity(BaseTestCase):
    def setUp(self):
        super(TestAmity, self).setUp()

    def tearDown(self):
        pass

    def test_total_number_of_people_increases(self):
        self.amity.add_person("Dennis", "fellows", True)
        self.amity.add_person("Gitare", "staff", True)

        assert self.amity.total_no_of_people == 2

    def test_total_number_of_rooms_increases(self):
        self.amity.add_room(["France", "Britain"], "offices")
        self.amity.add_room(["Germany"], "livingspaces")

        assert self.amity.total_no_of_rooms == 3

    def test_does_not_load_invalid_file(self):
        bad_filename = "badsample.txt"
        save_path = os.path.dirname(os.path.realpath(__file__)) + "/../app/userdata/"
        complete_name = os.path.join(save_path, bad_filename)

        bad_file_handle = open(complete_name, "w+")

        bad_file_handle.write("gibber not in \r\n good format")

        bad_file_handle.close()

        people_file = open(save_path + "badsample.txt")
        for line in people_file:
            self.amity.load_people(line)

        people_file.close()
        os.remove(save_path + "badsample.txt")

        assert self.amity.total_no_of_people == 0

    def test_loads_file(self):
        good_filename = "goodsample.txt"
        save_path = os.path.dirname(os.path.realpath(__file__)) + "/../app/userdata/"
        good_file = os.path.join(save_path, good_filename)
        good_file_handle = open(good_file, "w+")
        good_file_handle.write("OLUWAFEMI SULE FELLOW Y\r\nDOMINIC WALTERS STAFF")
        good_file_handle.close()

        people_file = open(save_path + "goodsample.txt")
        for line in people_file:
            self.amity.load_people(line)

        people_file.close()
        os.remove(save_path + "goodsample.txt")

        assert self.amity.total_no_of_people == 2

    def test_staff_cannot_want_accommodation(self):
        self.amity.add_person("Mbarak", "staff", True)

        self.assertDictEqual(
            self.amity.unbooked_people, {"offices": {"Mbarak", },
                                         "livingspaces": set()
                                        }
        )

    def test_does_not_add_person_twice(self):
        self.amity.add_person("Mbarak", "staff", False)
        self.amity.add_person("Mbarak", "staff", False)

        assert self.amity.total_no_of_people == 1

    def test_does_not_add_room_twice(self):
        self.amity.add_room(["France", "Britain", "France"], "offices")

        assert self.amity.total_no_of_rooms == 2

        self.amity.add_room(["France", "Britain", "France", "Russia"], "livingspaces")

        assert self.amity.total_no_of_rooms == 3

    def test_prints_allocation_to_file(self):
        self.amity.allocations = {
            "offices": {
                "America": set()
            },
            "livingspaces": {
                "Africa": set()
            }
        }
        self.amity.print_allocations("testfile")
        # Load file
        allocations_file_dir = os.path.dirname(os.path.realpath(__file__)) + "/../app/userdata/"
        complete_name = os.path.join(allocations_file_dir, "testfile.txt")
        allocations_file_handle = open(complete_name)

        test_string = []
        for line in allocations_file_handle:
            test_string.append(line)

        allocations_file_handle.close()
        os.remove(complete_name)
        assert test_string[1] == "America\n"

    def test_prints_unallocated_to_file(self):
        pass

    def test_does_not_overwrite_existing_file(self):
        allocations_file_dir = os.path.dirname(
            os.path.realpath(__file__)) + "/../app/userdata/"
        complete_name = os.path.join(allocations_file_dir, "test_overwrite.txt")
        file_handle = open(complete_name, "w+")

        assert not self.amity.save_to_file("test_overwrite", "one")
        file_handle.close()
        os.remove(complete_name)

    def test_clears_data(self):
        self.amity.people = {"fellows": {"Brian", },
                             "staff": {"Garfield", }
                             }
        self.amity.rooms = {"offices": {"America", },
                            "livingspaces": {"Java", }
                            }
        self.amity.unbooked_people = {"offices": set(),
                                      "livingspaces": set()
                                      }
        self.amity.allocations = {
            "offices": {"America": {"Brian", "Garfield"}},
            "livingspaces": {"Java": set()}
            }
        self.amity.clear_amity_data()

        self.assertDictEqual(self.amity.people, {"fellows": set(),
                                                 "staff": set()
                                                 })
        self.assertDictEqual(self.amity.rooms, {"offices": set(),
                                                "livingspaces": set()
                                                })
        self.assertDictEqual(self.amity.unbooked_people, {"offices": set(),
                                                          "livingspaces": set()
                                                          })
        self.assertDictEqual(self.amity.allocations, {"offices": {},
                                                      "livingspaces": {}
                                                      })
        assert not self.amity.total_no_of_people
        assert not self.amity.total_no_of_rooms

    def test_allocates_people(self):
        pass

    def test_does_not_allocate_without_rooms(self):
        pass

    def test_does_not_allocate_without_people(self):
        pass

    def test_allocates_person_when_added(self):
        pass


class TestRoom(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_cannot_add_more_than_six_occupants_to_office(self):
        pass

    def test_cannot_add_more_than_four_occupants_to_livingspace(self):
        pass


class TestPerson(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_does_not_reallocate_to_invalid_room(self):
        pass

    def test_does_not_reallocate_invalid_person(self):
        pass

    def test_staff_does_not_reallocate_to_livingspace(self):
        pass


if __name__ == "__main__":
    unittest.main()
