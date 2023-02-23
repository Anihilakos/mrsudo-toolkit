#!/usr/bin/python3
import time
import os
import base64


import requests


def notify_fsm(cr_event_id):
    url = "http://172.19.0.7:8080/event"

    payload = "event=" + str(cr_event_id)
    headers = {
        'Content-Type': 'text/plain'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def follow(thefile):
    """generator function that yields new lines in a file
    """
    # seek the end of the file
    thefile.seek(0, os.SEEK_END)

    # start infinite loop
    while True:
        # read last line of file
        line = thefile.readline()  # sleep if file hasn't been updated
        if not line:
            time.sleep(0.1)
            continue

        yield line


def cmd_execution_verification(line, verification_criterion_dict):
    # String manipulation, indicative line -> '29 08:23:03 3ed078394607 root: {"user": "root", "path": "/var/log",
    # "pid": "27", "b64_command": "bHMK", "status": "0", "b64_output": ""}'
    command = get_command_cmd_execution(line)
    user = get_user_cmd_execution(line)
    # print(verification_criterion_dict)
    print(verification_criterion_dict['user'] == user)
    print(verification_criterion_dict['command'] == command)
    print(verification_criterion_dict['command'] + " vs " + command)
    if verification_criterion_dict['user'] == user and verification_criterion_dict['command'] == command.strip():
        print('User event verified, send event ID to FSM')
        notify_fsm(verification_criterion_dict['cr_event'])


# function that extracts command criterion from the log
def get_command_cmd_execution(line):
    # keep all characters after 'b64_command'
    string1 = line[line.find('b64_command'):]
    # keep all characters before 'status'
    string2 = string1[:string1.find('status')]
    # clear special characters
    string3 = string2.replace('"', '').strip().strip(',')
    # keep only the b64 command
    b64_command = string3.replace('b64_command: ', '')
    # decode
    command = base64.b64decode(b64_command).decode('utf-8')
    # print(command)
    return command


# function that extracts user criterion from the log
def get_user_cmd_execution(line):
    # keep all characters after 'b64_command'
    string1 = line[line.find('user'):]
    # keep all characters before 'status'
    string2 = string1[:string1.find('path')]
    # clear special characters
    string3 = string2.replace('"', '').strip().strip(',')
    # keep only the b64 command
    user = string3.replace('user: ', '')
    print(user)
    return user


def load_verification_criteria_from_yaml(file_name):
    # Load YAML data from the file
    import yaml
    with open(file_name) as f:
        dict = yaml.load(f, Loader=yaml.FullLoader)
        print(dict)
        return dict


import click


@click.command()
@click.argument('file_name', type=click.Path(exists=True), required=True)
# @click.option('--log', '-l', required=False)
def event_captor_cmd_exec(file_name):
    # TODO Involve variable log name via -l option (not in the scope of the MVP)
    # TODO Stop mechanism for the captor (kill pid)
    logfile = open("/var/log/bash.log", "r")
    loglines = follow(logfile)
    # Load user event criteria

    # criteria for command execution are 'command' and 'user'
    # dummy_verification_criteria_dict = {"user": "root", "command": "whoami"}
    dummy_verification_criteria_dict = load_verification_criteria_from_yaml(file_name)
    for line in loglines:
        print(line)
        cmd_execution_verification(line, dummy_verification_criteria_dict)


if __name__ == '__main__':
    event_captor_cmd_exec()
