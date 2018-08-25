#!/bin/python

import subprocess
import argparse
import sys
import os
import time
import getpass
import pickle

class Pynotes:
    def __init__(self):
        if self.load_data():
            print('data from db loaded....')
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
        name = input('Name of the Note: ')
        note.set_name(name)
        print('Task creation...')
        while True:
            tasks_bool = input('Add task to the Note? (y/n): ')
            if tasks_bool == 'y':
                task_name = input('Name of the Task: ')
                note.add_task(task_name, False)
                continue
            elif tasks_bool == 'n':
                self.notes.append(note)
                self.save_data()
                break
            else:
                print('Unknown option selected. Try "y" or "n"')
                continue

    def check_task(self, note_id, task_id):
        self.notes[note_id].check_task(task_id)
        self.save_data()

    def print_notes(self):
        self.load_data()
        proc = subprocess.Popen(["stty", "size"], stdout=subprocess.PIPE)
        rows, cols = proc.stdout.read().strip().decode("utf-8").split()
        note_tuples = list()
        leftover_space = int(cols)
        for i, note in enumerate( self.notes ):
            str_note = note.str_repr(i)
            note_size = len(str_note[0])
            if leftover_space < note_size + 2 or len(note_tuples) == 0:
                leftover_space = int(cols) - note_size
                note_tuples.append(str_note)
            else:
                leftover_space -= 2 + note_size
                size_diff = len(str_note) - len(note_tuples[-1])
                if size_diff > 0:
                    for i in range(size_diff):
                        note_tuples[-1].append(' ' * len(note_tuples[-1][0]))
                last_line = 0
                for i,row in enumerate(str_note):
                    last_line = i
                    note_tuples[-1][i] += '  ' + row
                for i in range(last_line + 1, len(note_tuples[-1])):
                    note_tuples[-1][i] += '  ' + ' ' * note_size

        for glued_note in note_tuples:
            for row in glued_note:
                print(row)
            print()


class Note:
    def __init__(self):
        self.name = ''
        self.timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
        self.tasks = list()
    def set_name(self, name):
        self.name = name
    def add_task(self, task_name, done=False ):
        task = [task_name, done]
        self.tasks.append(task)
    def check_task(self, task_id):
        self.tasks[task_id][1] = not self.tasks[task_id][1]
    def str_repr(self, i):
        if len(self.tasks) > 0:
            max_width = max(len(self.name), len(self.timestamp), max([len(x[0]) + 3 + len(str(i)) for i,x in enumerate(self.tasks)]))
        else:
            max_width = max(len(self.name), len(self.timestamp))
        str_repr = list()
        str_repr.append('+' + '=' * (max_width + 2) + '+')
        str_repr.append('|' + ' #' + str(i) + ' ' * (max_width - len(str(i))) + '|')
        str_repr.append('|' + ' ' + self.name + ' ' * (max_width - len(self.name)) + ' ' + '|')
        str_repr.append('+' + '=' * (max_width + 2) + '+')
        for i, task in enumerate(self.tasks):
            mark = ' '
            if task[1]:
                mark = '*'
            str_repr.append('| ' + str(i) + ' ' + task[0] + ' ' * (max_width - len(task[0]) - 2 - len(str(i))) + mark + ' ' + '|')
        if len(self.tasks):
            str_repr.append('+' + '=' * (max_width + 2) + '+')
        return str_repr

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="command to run")
    parser.add_argument("-n", help="specify note to select")
    parser.add_argument("-t", help="specify task to select")
    args = parser.parse_args()
    if args.c is None:
        print("No argument given...try --help")
        sys.exit(1)
    if args.c == 'add':
        command = 'add'
    elif args.c == 'list':
        command = 'list'
    elif args.c == 'check':
        if args.n is None or args.t is None:
            print('You must specify note number with -n ... and task number with -t')
            sys.exit(1)
        command = 'check'
    else:
        print('Unrecognized command, try --help')
        sys.exit(1)

    instance = Pynotes()
    if command == 'add':
        instance.add_note()
    elif command == 'list':
        os.system('cls' if os.name == 'nt' else 'clear')
        instance.print_notes()
    elif command == 'check':
        instance.check_task(int(args.n), int(args.t))

    sys.exit(0)
