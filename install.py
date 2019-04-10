#!/usr/bin/env python3

import os
import shutil
from subprocess import Popen, PIPE


def sh(li_cmd):
    output, _ = Popen(li_cmd, stdout=PIPE, encoding='utf-8') \
        .communicate(timeout=10)
    return output.rstrip()


def check_anwser(check_anwser):
    return check_anwser.lower() in ['', 'y', 'yes']


def install(user, python_path):
    install_dir = 'systemd_to_install'
    shutil.copytree('systemd', install_dir)
    for file in os.listdir(install_dir):
        with open(install_dir + '/' + file, 'r') as f:  # r+ not overwrite
            to_write = f.read() \
                .replace('user_name', user) \
                .replace('path/to/python', python_path)
        with open(install_dir + '/' + file, 'w') as f:
            f.write(to_write)
    print('\ndirectory: "{}" created'.format(install_dir))


def main():
    user = sh(['whoami'])
    python_path = sh(['which', 'python3'])
    print('user: {}\npython environment: {}'.format(user, python_path))
    is_ok = input('does these info are correct' +
                  ' to run lswf from systemd service ? [Y/n] ')

    if check_anwser(is_ok):
        install(user, python_path)
    else:
        print('the user is you (whoami), and python environment is' +
              ' which python3 is given by the command `which python3`\n' +
              'Activate the desired python venv to change this path')


if __name__ == '__main__':
    main()
