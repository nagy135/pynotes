#!/bin/python

import subprocess
import argparse
import os
import time
import getpass

def db_add():
    name = input('Name of the note: ')
    subnotes = []
    time_stamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
    subnotes_loop = True
    while subnotes_loop:
        have_subnotes = input('Does this note have subnotes? (y/n): ')
        if have_subnotes == 'y':
            subnotes_loop = False
            subnotes_adding_loop = True
            print('Keep typing names of subnotes, or type "exit": ')
            while subnotes_adding_loop:
                subnote_name = input('Name of subnote: ')
                if subnote_name == 'exit' or subnote_name == '':
                    subnotes_adding_loop = False
                else:
                    subnotes.append(subnote_name)

        elif have_subnotes == 'n':
            subnotes_loop = False
        else:
            print('Bad option ... try (y/n): ')

    print('Creation finished...')
    home_folder = os.path.expanduser("~")
    directory = home_folder + '/.config/pynotes/'
    with open(directory + 'pynotes_db','a') as db:
        db.write(name + '\n')
        db.write(time_stamp + '\n')
        for subnote in subnotes:
            db.write(subnote + ' 0 \n')
        db.write('\n')

def db_list(note_id=None):
    home_folder = os.path.expanduser("~")
    directory = home_folder + '/.config/pynotes/'
    with open(directory + 'pynotes_db','r') as db:
        notes = False
        name_bool = False
        time_bool = False
        order = 0
        data_notes = []
        for line in db:
            line = line.strip()
            subnotes = []
            if line == '' and not notes:
                continue
            if notes:
                if not name_bool:
                    name = line
                    name_bool = True
                    data_notes.append([])
                    data_notes[order].append(name)
                elif not time_bool:
                    timestamp = line
                    time_bool = True
                    data_notes[order].append(timestamp)
                    data_notes[order].append([])
                elif line == '':
                    name_bool = False
                    time_bool = False
                    order += 1
                else:
                    data_notes[order][2].append(line)
            elif line == 'notes:':
                notes = True
    if note_id is not None:
        for i, note in enumerate(data_notes):
            if i != note_id:
                data_notes[i] = []
    return data_notes

def print_db_list(data):
    for note_id, note in enumerate(data):
        if note == []:
            continue
        name = note[0]
        timestamp = note[1]
        subnotes = note[2]
        try:
            longest_subnote = max([len(x) for x in note[2]])
        except ValueError:
            longest_subnote = 0
        longest = max(len(name), len(timestamp), longest_subnote)

        print(' +' + '-' * (longest + 2) + '+')
        print(' | #' + str(note_id) + ' ' * (longest - (len(str(note_id))) - 1) + ' |')
        left_padding = (longest - len(name)) // 2
        right_padding = (longest - len(name) - left_padding)
        print(' |-' + '-' * left_padding + name + '-' * right_padding + '-|')
        print(' | ' + timestamp + ' ' * (longest - len(timestamp) ) + ' |')
        if len(subnotes) > 0:
            print(' |=' + '=' * longest + '=|')
        for subnote in subnotes:
            subnote_name = ' '.join(subnote.split()[:-1])
            subnote_val = int(subnote.split()[-1])
            checked = ' '
            if subnote_val:
                checked = '+'
            print(' | ' + subnote_name + ' ' * (longest - len(subnote_name) ) + checked + '|')
        print(' +' + '-' * (longest + 2) + '+')
        print()

def db_remove(note_id):
    home_folder = os.path.expanduser("~")
    directory = home_folder + '/.config/pynotes/'
    if not os.path.exists(directory):
        print('Use init first !')
        return
    notes = db_list()
    del notes[note_id]
    with open(directory + 'pynotes_db','r') as db:
        lines = db.readlines()[:5]
    with open(directory + 'pynotes_db','w') as db:
        for line in lines:
            db.write(line)
        for note in notes:
            db.write(note[0] + '\n')
            db.write(note[1] + '\n')
            for subnote in note[2]:
                db.write(subnote + '\n')
            db.write('\n')


def initialize():
    print('Initializing...')
    home_folder = os.path.expanduser("~")
    directory = home_folder + '/.config/pynotes/'
    if not os.path.exists(directory):
        print('Creating directory structure {}'.format(directory))
        os.makedirs(directory)
    print('Creating {}pynotes_db file'.format(directory))
    with open(directory + 'pynotes_db','w') as db:
        username = getpass.getuser()
        db.write('# This file is storage place for notes\n')
        db.write('# Created by user: {}\n'.format(username))
        time_stamp = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
        db.write('# Creation time: {}\n'.format(time_stamp))
        db.write('\n')
        db.write('notes:\n')


if __name__ == '__main__':

    proc = subprocess.Popen(["stty", "size"], stdout=subprocess.PIPE)
    rows, cols = proc.stdout.read().strip().decode("utf-8").split()

    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="command to run", choices=['init', 'add', 'list', 'remove'])
    parser.add_argument("-id", help="id of note show (use with list)", type=int)
    # parser.add_argument("-a", help="file is in absolute path format", action="store_true")
    # parser.add_argument("-o", help="name of background file(default = file + _bg)")
    args = parser.parse_args()
    if args.command == 'init':
        initialize()
    elif args.command == 'add':
        db_add()
    elif args.command == 'list':
        data_notes = db_list(args.id)
        print_db_list(data_notes)
    elif args.command == 'remove':
        if args.id is not None:
            db_remove(args.id)
        else:
            print('Specify note id, try "list" command')
    else:
        print('Unrecognized command, try --help')
