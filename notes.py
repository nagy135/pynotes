#!/bin/python

import subprocess
import argparse
import sys
import os
import time
import getpass
import pickle
import time

class Pynotes:
    def __init__(self):
        if self.load_data():
            print('data loaded')
        else:
            print('empty db created')
            self.save_data()

    def create_db(self):
        print('initializing...')
        home_folder = os.path.expanduser("~")
        directory = home_folder + '/.config/pynotes/'
        if not os.path.exists(directory):
            print('Creating directory structure {}'.format(directory))
            os.makedirs(directory)
        print('Creating {}db.dat file'.format(directory))
        self.save_data()

    def load_data(self):
        try:
            home_folder = os.path.expanduser("~")
            directory = home_folder + '/.config/pynotes/'
            with open(directory + "db.dat", "rb") as t:
                self.notes = pickle.load(t)
            return True
        except Exception as e:
            print(e)
            self.notes = list()
            self.create_db()
            return False

    def save_data(self):
        home_folder = os.path.expanduser("~")
        directory = home_folder + '/.config/pynotes/'
        with open(directory + "db.dat", "wb") as t:
            pickle.dump(self.notes, t)

    def add_note(self):
        note = Note()
        input('Name of the Note: ')

    def print_notes(self):
        pass

class Note:
    def __init__(self):
        self.name = ''
        self.timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
        self.tasks = list()
    def set_name(self, name):
        self.name = name
    def add_task(self, task_name, )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="command to run")
    args = parser.parse_args()
    if args.c is None:
        print("No argument given...try --help")
        sys.exit(1)
    if args.c == 'add':
        command = 'add'
    elif args.c == 'list':
        command = 'list'
    else:
        print('Unrecognized command, try --help')
        sys.exit(1)

    instance = Pynotes()
    if command == 'add':
        instance.add_note()
    elif command == 'list':
        instance.print_notes()

    sys.exit(0)
