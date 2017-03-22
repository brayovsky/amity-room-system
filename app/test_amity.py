from unittest import TestCase
import unittest
from basetest import BaseTestCase
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
        save_path = os.path.dirname(os.path.realpath(__file__)) + "/userdata/"
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
        save_path = os.path.dirname(os.path.realpath(__file__)) + "/userdata/"
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
        pass

    def test_does_not_overwrite_existing_file(self):
        pass

    def test_creates_database(self):
        pass

    def test_resets_database(self):
        pass

    def test_checks_for_existing_database(self):
        pass

    def test_does_not_show_state_with_debug_off(self):
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
