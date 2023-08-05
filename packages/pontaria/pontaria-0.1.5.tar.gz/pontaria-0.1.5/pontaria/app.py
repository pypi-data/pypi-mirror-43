#!/usr/bin/env python
from pontaria.auth import gc
from pontaria.date_utils import get_period, sum_hours
from functools import reduce
import arrow 
import os
from sys import argv
import json

# Checks and creates dir
DIR_PATH = os.path.expanduser('~') + "/.pontaria"
if not os.path.exists(DIR_PATH):
    os.makedirs(DIR_PATH)
SPREADSHEET_ID = '1F-1MZopQ3nCT-LdSIRTs8khDC2Rp8r96AFHaH2eVIm4'
LOG_FILE = open(f"{DIR_PATH}/logs-" + arrow.now().format("YYYY-MM-DD"), 'a+')
CONFIG_FILE = open(f"{DIR_PATH}/config.json",'r+',encoding='utf-8')
SESSION_FILE = open(f"{DIR_PATH}/session.json", 'r+',encoding='utf-8')

CONFIGS = {}
if os.path.getsize(f"{DIR_PATH}/config.json") > 0:
    CONFIGS = json.load(CONFIG_FILE)
if 'sheetname' not in CONFIGS:
    sheetname = input("Please provide the sheetname (your name probably)\n\t> ")
    CONFIGS = { "sheetname":sheetname }
    json.dump(CONFIGS, CONFIG_FILE)
ws = gc.open(CONFIGS['sheetname'])
sh = ws.worksheet(get_period())

def get_range():
    return f'{get_period()}!A4:G1000'

def get_hours_worked(rows):
    return sum_hours([row[4] for row in rows])

def get_sheet_values():
    # pylint: disable=no-member
    # spreadsheets instance
    # getting sheets title from the spreadsheet
    values = sh.get_all_values()[2:]
    filtered_values = list(filter(lambda row: row[0], values))
    mapped_values = [ [row[0], row[1], row[2], row[3], row[5][:5]] for row in filtered_values ]
    return mapped_values

def analytics():
    values = get_sheet_values()
    hours_worked = get_hours_worked(values)
    past_payment = (arrow.now() - arrow.get(2019, 2, 20)).days 
    days_until = (arrow.get(2019, 3, 21) - arrow.now()).days
    prevision = (hours_worked / past_payment) * days_until
    print(f'''
    PERIOD: {get_period()}
    Days remaining: {days_until} days
    Hours worked until now: {hours_worked}h
    Gains until now: R${hours_worked * 11.36}
    Prevision: R${(prevision + hours_worked) * 11.36}
''')

def log(action):
    LOG_FILE.write(f"{arrow.now().format()}, {action}\n")

def shift_set_session(activity):
    SESSION_FILE.truncate()
    json.dump({
        "datetime": arrow.now().format(),
        "activity": activity
    }, SESSION_FILE)

def start_shift():
    shift_start = arrow.now()
    activity = None
    try:
        activity = argv[2]
        pass
    except:
        pass
    shift_set_session(activity)
    log(f"STARTING SHIFT,{activity if activity else ''},")
    print(f"Starting shift at {shift_start.format()}")
    if activity:
        print("[ACTIVITY]", activity)
    print("Have a great shift!")

def commit_shift():
    # checks if session file is empty
    if not os.path.getsize(f"{DIR_PATH}/session.json"):
        answer = input("You haven't started a shift yet, wanna do it now? [Y/n]: ")
        if answer in ('y', 'Y', ''):
            start_shift()
            return
        else:
            return

    # read shift session
    session = json.load(SESSION_FILE)
    today = arrow.now().format('DD/MM/YYYY')
    session_start = arrow.get(session['datetime'])
    session_end = arrow.now()
    session_delta = session_end - session_start
    # Format session delta
    delta_seconds = session_delta.seconds
    delta_hours = delta_seconds // 3600
    delta_minutes = (delta_seconds - delta_hours * 3600) // 60
    delta_formatted = f"{delta_hours:02d}:{delta_minutes:02d}"
    # Get activity
    session_activity = session['activity']
    if not session_activity:
        if len(argv) >= 3:
            session_activity = argv[2]
        else:
            session_activity = input("Provide a activity description for the shift\n\t> ")
    # Format row
    row = [today, session_activity, session_start.format('HH:mm'), session_end.format('HH:mm'), '', delta_formatted, '']
    append_row(row)
    open(f"{DIR_PATH}/session.json", "w").close()
    # Print confirmation
    print("Great work!")

def append_row(row):
    cells = sh.findall('')
    first_empty_cell = None
    for cell in cells:
        if cell.col == 1 and cell.row >= 3:
            first_empty_cell = cell
            break
    if first_empty_cell:
        sh.insert_row(row, index=first_empty_cell.row, value_input_option='USER_ENTERED')
    else:
        rows_len = len(sh.get_all_values())
        sh.insert_row(row, index=rows_len+1, value_input_option='USER_ENTERED')

def main():
    if len(argv) > 1:
        first_arg = argv[1]
        if first_arg == 'start' or first_arg == 's':
            start_shift()
        if first_arg == 'commit' or first_arg == 'c':
            commit_shift()
        if first_arg == 'analytics' or first_arg == 'a':
            analytics()
    # print(sh.worksheets())
    SESSION_FILE.close()
    CONFIG_FILE.close()
    LOG_FILE.close()
    pass

if __name__ == '__main__':
    main()