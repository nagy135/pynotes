import os
import time
import sys

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
            status = 'completed'
        else:
            status = 'not completed'
        print(status)
        while True:
            resp = input('New status (y = completed / n = not):\n')
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
