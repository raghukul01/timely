#! /usr/bin/env python

import argparse
from datetime import datetime, date, timedelta
import time
import pandas as pd
from tabulate import tabulate


# parse the params passed
parser = argparse.ArgumentParser(description='Track your time efficiently')

parser.add_argument('--list', action="store_true", default=False, help='Lists out all the activity for the day')
parser.add_argument('--current', action="store_true", default=False, help='Current task')
parser.add_argument('--add', action="store_true", default=False, help='Add a new task')
parser.add_argument('--stop', action="store_true", default=False, help='stop all running tasks')
parser.add_argument('--name', help='Activity name')


# state 1 means activity is running, -1 mean it ends
cols = ['date', 'task', 'state', 'time']

try:
    df = pd.read_csv('time.log')
    df['time'] = pd.to_datetime(df['time'])
    df['state'] = df['state'].astype('int')
except:
    df = pd.DataFrame(columns=cols)


def current():
    global df
    tasks = list(df['task'])
    tasks = list(dict.fromkeys(tasks))
    for task in tasks:
        count = int(df.loc[df['task'] == task]['state'].sum())
        if count == 1:
            return task
    return None


def add(task_name):
    global df
    # check if the task is already running
    if(task_name == current()):
        print('task already running.')
        return
    new_task = {}
    new_task['time'] = datetime.now()
    new_task['date'] = date.today()
    new_task['task'] = task_name
    new_task['state'] = 1

    df = df.append(new_task, ignore_index=True)
    print('Task "' + task_name + '" added.')


def stop():
    global df
    running = current()
    if running is None:
        print('No task running.')
    else:
        new_task = {}

        new_task['time'] = datetime.now()
        new_task['date'] = date.today()
        new_task['task'] = running
        new_task['state'] = -1

        df = df.append(new_task, ignore_index=True)
        print('Stopped task:', running)


def get_duration(task_name):
    global df
    if task_name is None:
        return timedelta(0)
    checkpoints = []
    for i in range(len(df)):
        if(df['task'].iloc[i] == task_name):
            instance = df['time'].iloc[i]
            state = df['state'].iloc[i]
            checkpoints.append([instance, state])

    duration = datetime.now()
    for record in checkpoints:
        if record[1] == 1:
            duration -= record[0]
        else:
            duration += record[0]
    if(checkpoints[-1][1] == -1):
        duration -= datetime.now()
    return duration


def current_activity():
    curr = current()
    duration = get_duration(curr)
    duration = str(duration).split('.')[0]
    print(tabulate([[str(curr), duration]], headers=['Activity', 'Duration']))


def listall():
    tasks = list(df['task'])
    tasks = list(dict.fromkeys(tasks))
    tasks.sort()
    curr = current()

    header = ['Activity', 'Duration', 'Running']
    data = []

    for task in tasks:
        duration = get_duration(task)
        duration = str(duration).split('.')[0]
        if(task == curr):
            symbol = 'x'
        else:
            symbol = '-'
        data.append([task, duration, symbol])
    print(tabulate(data, headers=header))


args = parser.parse_args()

if args.add:
    if args.name is None:
        print('No activity name provided.')
    else:
        add(args.name)

if args.stop:
    stop()

if args.list:
    listall()

if args.current:
    current_activity()

df.to_csv('time.log', index=False)
