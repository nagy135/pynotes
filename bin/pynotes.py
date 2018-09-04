from .note import Note
import os
import pickle
import sys
import subprocess

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

    def swap_notes(self, first, second):
        self.notes[int(first)], self.notes[int(second)] = self.notes[int(second)], self.notes[int(first)]
        self.save_data()
    def swap_tasks(self, note, first, second):
        self.notes[int(note)].tasks[int(first)], self.notes[int(note)].tasks[int(second)] = self.notes[int(note)].tasks[int(second)], self.notes[int(note)].tasks[int(first)]
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
            if i != (len(notes) - 1):
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
                leftover_space = int(cols) - (note_size + 2)
                note_tuples.append(str_note)
            else:
                leftover_space -= (2 + note_size)
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
            if len(glued_note[0]) > int(cols):
                print('Not enough space to fit notes on screen')
                sys.exit(1)
        for glued_note in note_tuples:
            for row in glued_note:
                print(row)
            print()
