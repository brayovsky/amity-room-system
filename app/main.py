#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
Usage:
    Amity create_room (-o | --office | -l | --livingspace) <room_name>...
    Amity add_person <person_name> (-f | --fellow | -s | --staff) [wants_accommodation]
    amity allocate_people
    Amity reallocate_person <person_identifier> <new_room_name>
    Amity load_people <text_file>
    Amity print_allocations [-o] [<filename>]
    Amity print_unallocated [-o] [<filename>]
    Amity print_room <room_name>
    Amity save_state [--db=sqlite_database]
    Amity load_state <sqlite_database>
    Amity (-i | --interactive)
    Amity (-h | --help | --version)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import cmd
from docopt import docopt, DocoptExit
from Amity import Amity
from Person import Person


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.
            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class AmityInteractive (cmd.Cmd):
    intro = 'Welcome to Amity!'
    prompt = '(Amity)'

    @docopt_cmd
    def do_create_room(self, arg):
        """Usage: create_room (-o | --office | -l | --livingspace) <room_name>..."""

        rooms = arg["<room_name>"]

        if arg["-l"] or arg["--livingspace"]:
            amity.add_room(rooms, "livingspaces")
        elif arg["-o"] or arg["--office"]:
            amity.add_room(rooms, "offices")

    @docopt_cmd
    def do_add_person(self, arg):
        """Usage: add_person <person_name> (-f | --fellow | -s | --staff) [wants_accommodation]"""
        person_name = arg["<person_name>"]
        wants_accommodation = arg["wants_accommodation"]

        if arg["-s"] or arg["--staff"]:
            amity.add_person(person_name, "staff", wants_accommodation)
        elif arg["-f"] or arg["--fellow"]:
            amity.add_person(person_name, "fellows", wants_accommodation)

    @docopt_cmd
    def do_allocate_people(self, arg):
        """Usage: allocate_people"""
        amity.allocate()

    @docopt_cmd
    def do_reallocate_person(self, arg):
        """Usage: reallocate_person <person_identifier> <new_room_name>"""
        person = Person(arg["<person_identifier>"])
        person.change_room(arg["<new_room_name>"], amity)

    @docopt_cmd
    def do_load_people(self, arg):
        """Usage: load_people <text_file>"""
        try:
            people_file = open(arg["<text_file>"])
        except FileNotFoundError:
            print("File '{}' not found".format(arg["<text_file>"]))
            return

        for line in people_file:
            # Call method for processing file into proper output and use existing functions DRY!!
            amity.load_people(line)

        people_file.close()

    @docopt_cmd
    def do_print_allocations(self, arg):
        """Usage: print_allocations [-o] [<filename>]"""
        if arg["-o"] and arg["<filename>"]:
            amity.print_allocations(arg["<filename>"])
            return
        amity.print_allocations()

    @docopt_cmd
    def do_print_unallocated(self, arg):
        """Usage: print_unallocated [-o] [<filename>]"""
        if arg["-o"] and arg["<filename>"]:
            amity.print_unallocated(arg["<filename>"])
            return
        amity.print_unallocated()

    @docopt_cmd
    def do_print_room(self, arg):
        """Usage: print_room <room_name>"""
        amity.print_room(arg["<room_name>"])

    @docopt_cmd
    def do_save_state(self, arg):
        """Usage: save_state [--db=sqlite_database]"""
        print("Should persist all data to a sqlite database")
        print(arg)
        amity.save_amity(arg["--db"])

    @docopt_cmd
    def do_load_state(self, arg):
        """Usage: load_state <sqlite_database>"""
        print("Should load data from a sqllite db provided")

    @docopt_cmd
    def do_quit(self, arg):
        """Usage: (quit)"""
        print('Good Bye!')
        exit()


if __name__ == '__main__':
    opt = docopt(__doc__, argv="-i")
    amity = Amity()
    AmityInteractive().cmdloop()

