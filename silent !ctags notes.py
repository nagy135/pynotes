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
            # print('data from db loaded....')
            pass
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

    def _remove(self, note_id, task_id=None):
        if task_id is None:
            self.notes.remove(self.notes[note_id])
            print('Note successfully removed')
        else:
            self.notes[note_id].remove_task(task_id)
            print('Task successfully removed')
        self.save_data()

    def edit(self, note_id, task_id=None):
        if task_id is not None:
            self.notes[note_id].edit_task(task_id)
        if note_id is not None and task_id is None:
            print('Current name: ' + self.notes[note_id].name)
            new_name = input('New name of the Task: ')
            self.notes[note_id].name = new_name
        self.save_data()

    def desc(self, note_id):
        note = self.notes[note_id]
        with open('/tmp/pynote_description_edit', 'w') as t:
            if len(note.desc.strip()) > 0:
                t.write(note.desc)
        os.system('{} /tmp/pynote_description_edit'.format(os.getenv('EDITOR')))
        with open('/tmp/pynote_description_edit', 'r') as t:
            note.desc = ''.join(t.readlines())
        self.save_data()

    def add(self, note_id=None):
        if note_id is None:
            self.add_note()
        else:
            self.notes[note_id].add_task()
            self.save_data()

    def add_note(self):
        note = Note()
        name = input('Name of the Note: ')
        note.set_name(name)
        print('Task creation...')
        note.add_task()
        self.notes.append(note)
        self.save_data()

    def check_task(self, note_id, task_id):
        self.notes[note_id].check_task(task_id)
        self.save_data()

    def list_notes(self):
        print('All notes:')
        print()
        for i, note in enumerate( self.notes ):
            note.basic_print(i)

    def tree(self, note_id=None, status=False):
        if note_id is None:
            notes = self.notes
        else:
            notes = [self.notes[note_id]]
        for i, note in enumerate( notes ):
            note.basic_print(i, tasks=False)
            note.tree_print(status)
            if i != (len(self.notes) - 1):
                print('-' * 20)

    def print_notes(self, i=None):
        proc = subprocess.Popen(["stty", "size"], stdout=subprocess.PIPE)
        rows, cols = proc.stdout.read().strip().decode("utf-8").split()
        note_tuples = list()
        leftover_space = int(cols)
        if i is None:
            notes = self.notes
        else:
            notes = [self.notes[i]]
        for i, note in enumerate( notes ):
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
                if len(row) > int(cols):
                    print('Not enough space to fit notes on screen')
                    sys.exit(1)
        for glued_note in note_tuples:
            for row in glued_note:
                print(row)
            print()


class Note:

    def __init__(self):
        self.name = ''
        self.timestamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
        self.tasks = list()
        self.desc = ''

    def set_name(self, name):
        self.name = name

    def add_task(self):
        while True:
            tasks_bool = input('Add task to the Note? (y/n): ')
            if tasks_bool == 'y':
                task_name = input('Name of the Task: ')
                self.tasks.append([task_name, False])
                continue
            elif tasks_bool == 'n':
                break
            else:
                print('Unknown option selected. Try "y" or "n"')
                continue
        return

    def check_task(self, task_id):
        self.tasks[task_id][1] = not self.tasks[task_id][1]

    def remove_task(self, task_id):
        del self.tasks[task_id]

    def edit_task(self, task_id):
        self.tasks[task_id][0]
        print('Current text is:')
        print(self.tasks[task_id][0])
        self.tasks[task_id][0] = input('New text:\n')
        print('Current status is:')
        if self.tasks[task_id][1]:
            status = 'done'
        else:
            status = 'not done'
        print(status)
        while True:
            resp = input('New status(y/n):\n')
            if resp == 'y':
                self.tasks[task_id][1] = True
                break
            elif resp == 'n':
                self.tasks[task_id][1] = False
                break
            else:
                print('Wrong option, try (y/n)')

    def tree_print(self, status_bool=False):
        for i,task in enumerate(self.tasks):
            leaf = str(i) + ' - ' + task[0]
            status = ' '
            if status_bool and task[1]:
                status = '*'
            if status and task[1]:
                leaf += ' - done'
            if i == 0:
                if len(self.tasks) == 1:
                    print(status + '└──' + ' ' + leaf)
                else:
                    print(status + '├──' + ' ' + leaf)
                pass
            elif i == (len(self.tasks) - 1):
                print(status + '└──' + ' ' + leaf)
                pass
            else:
                print(status + '├──' + ' ' + leaf)

    def basic_print(self, i, tasks=True):
        if tasks:
            print('#' + str(i) + ' ' + self.name + ', tasks: ' + str(len(self.tasks)))
        else:
            print('#' + str(i) + ' ' + self.name)

    def str_repr(self, i):
        if len(self.tasks) > 0:
            max_width = max(len(self.name), len(self.timestamp), max([len(x[0]) + 3 + len(str(i)) for i,x in enumerate(self.tasks)]))
        else:
            max_width = max(len(self.name), len(self.timestamp))

        if len(self.desc.strip()) > 0:
            for line in self.desc.strip().split('\n'):
                if len(line) > max_width:
                    max_width = len(line)

        str_repr = list()
        str_repr.append('+' + '=' * (max_width + 2) + '+')
        str_repr.append('|' + ' #' + str(i) + ' ' * (max_width - len(str(i))) + '|')
        right_padding = (max_width - len(self.name)) // 2
        left_padding = (max_width - len(self.name)) - right_padding
        if right_padding < left_padding:
            right_padding, left_padding = left_padding, right_padding
        str_repr.append('|' + ' ' + ' ' * left_padding + self.name + ' ' * right_padding + ' ' + '|')
        str_repr.append('+' + '-' * (max_width + 2) + '+')
        str_repr.append('|' + ' ' + self.timestamp + ' ' * (max_width - len(self.timestamp)  + 1) + '|')
        str_repr.append('+' + '=' * (max_width + 2) + '+')

        if len(self.desc.strip()) > 0:
            for line in self.desc.strip().split('\n'):
                str_repr.append('|' + ' ' + line + ' ' * (max_width - len(line)) + ' ' + '|')
            str_repr.append('+' + '=' * (max_width + 2) + '+')

        for i, task in enumerate(self.tasks):
            mark = ' '
            if task[1]:
                mark = '*'
            str_repr.append('+ ' + str(i) + ' ' + task[0] + ' ' * (max_width - len(task[0]) - 2 - len(str(i))) + mark + ' ' + '+')
        if len(self.tasks):
            str_repr.append('+' + '=' * (max_width + 2) + '+')
        return str_repr

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", help="command to run", choices=['add', 'print', 'list', 'remove', 'check', 'tree', 'edit', 'desc'])
    parser.add_argument("-n", help="specify note to select")
    parser.add_argument("-s", help="show status of notes", action="store_true")
    parser.add_argument("-r", help="repaint, clear terminal", action="store_true")
    parser.add_argument("-t", help="specify task to select")
    args = parser.parse_args()
    if args.c is None:
        print("No argument given...try --help")
        sys.exit(1)
    if args.c == 'add':
        command = 'add'
    elif args.c == 'print':
        command = 'print'
    elif args.c == 'list':
        command = 'list'
    elif args.c == 'tree':
        command = 'tree'
    elif args.c == 'edit':
        command = 'edit'
    elif args.c == 'remove':
        command = 'remove'
    elif args.c == 'desc':
        command = 'desc'
    elif args.c == 'check':
        if args.n is None or args.t is None:
            print('You must specify note number with -n ... and task number with -t')
            sys.exit(1)
        command = 'check'
    else:
        print('Unrecognized command, try --help')
        sys.exit(1)

    if args.r:
        os.system('cls' if os.name == 'nt' else 'clear')
    instance = Pynotes()
    if command == 'add':
        if args.n is None:
            instance.add()
        else:
            instance.add(int(args.n))
    elif command == 'print':
        if args.n is None:
            instance.print_notes(args.n)
        else:
            instance.print_notes(int(args.n))
    elif command == 'remove':
        if args.n is None and args.t is None:
            print('You have to specify -n (possible with -t to remove task)')
            sys.exit(1)
        if args.t is None:
            instance._remove(int(args.n))
        else:
            instance._remove(int(args.n), int(args.t))
    elif command == 'edit':
        if args.n is None and args.t is None:
            print('You have to specify -n (possible with -t to edit task)')
            sys.exit(1)
        if args.t is None:
            instance.edit(int(args.n))
        else:
            instance.edit(int(args.n), int(args.t))
    elif command == 'desc':
        if args.n is None:
            print('You have to specify note (with -n) to add/edit description on')
            sys.exit(1)
        instance.desc(int(args.n))
    elif command == 'tree':
        if args.n is not None:
            note_id = int(args.n)
        else:
            note_id = None
        if args.s:
            instance.tree(note_id, status=True)
        else:
            instance.tree(note_id)
    elif command == 'list':
        instance.list_notes()
    elif command == 'check':
        instance.check_task(int(args.n), int(args.t))

    sys.exit(0)
