# amity-room-system
Amity room allocation system is a console application for assigning office and living spaces in a facility.

The building blocks are:

* Python 3
* Docopts

## Setting Up for Development
* prepare directory for project code and virtualenv:

        $ mkdir -p ~/amity
        $ cd ~/amity

* prepare virtual environment

        $ virtualenv --python=python3 venv
        $ source venv/bin/activate

* check out project code:

        $ git clone https://github.com/brayovsky/amity-room-system.git

* install requirements into virtualenv:

        $ pip install -r amity/requirements.txt

* run the app:

        $ python amity/app/main.py

The app should run normally

## Using the app
Once you have run the app type `help` to see available commands. The commands are:

    Amity create_room (-o | --office | -l | --livingspace) <room_name>...
    Amity add_person <first_name> [<last_name>] (-f | --fellow | -s | --staff) [--wants_accommodation=N]
    Amity allocate_people
    Amity reallocate_person <new_room_name> <first_name> [<last_name>]
    Amity load_people <text_file>
    Amity print_allocations [-o] [<filename>]
    Amity print_unallocated [-o] [<filename>]
    Amity print_room <room_name>
    Amity save_state [--db=sqlite_database]
    Amity load_state <sqlite_database>

To run tests and check for test coverage, run

        nosetests test/ --with-coverage

Settings are located in the file `app/settings.py`. To check on the state of amity(show rooms, allocations etc) when you run a command set

        DEBUG = True

