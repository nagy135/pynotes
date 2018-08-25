#!/bin/python

import argparse
import sys
import os
from bin.pynotes import Pynotes

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
