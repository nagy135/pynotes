import subprocess
import argparse
import os
import time
import getpass

def add():
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

def db_list():
    print('Parsing db records...')
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
    print_db_list(data_notes)

def print_db_list(data):
    for note_id, note in enumerate(data):
        name = note[0]
        timestamp = note[1]
        subnotes = note[2]
        longest_subnote = max([len(x) for x in note[2]])
        longest = max(len(name), len(timestamp), longest_subnote)

        print('#' * (longest + 4))
        print('# #' + str(note_id) + ' ' * (longest - (len(str(note_id))) - 1) + ' #')
        left_padding = (longest - len(name)) // 2
        right_padding = (longest - len(name) - left_padding)
        print('# ' + '-' * left_padding + name + '-' * right_padding + ' #')
        print('# ' + timestamp + ' ' * (longest - len(timestamp) ) + ' #')
        print('#_' + '_' * longest + '_#')
        for subnote in note[2]:
            subnote_name = ' '.join(subnote.split()[:-1])
            subnote_val = int(subnote.split()[-1])
            checked = ' '
            if subnote_val:
                checked = '+'
            print('# ' + subnote_name + ' ' * (longest - len(subnote_name) ) + checked + '#')
        print('#' * (longest + 4))
        print()

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
    parser.add_argument("command", help="command to run")
    # parser.add_argument("-i", help="number of iterations(default = 5)", type=int)
    # parser.add_argument("-a", help="file is in absolute path format", action="store_true")
    # parser.add_argument("-o", help="name of background file(default = file + _bg)")
    args = parser.parse_args()
    if args.command == 'init':
        initialize()
    elif args.command == 'add':
        add()
    elif args.command == 'list':
        db_list()
    else:
        print('Unrecognized command, try --help')
