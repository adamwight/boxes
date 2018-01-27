"""
Framework for extensible actions
"""

import importlib
import os.path
import re
import sys

from boxes import config

node_commands = []


class NodeCommand(object):
    def get_key(self):
        raise NotImplementedError()

    def get_description(self):
        raise NotImplementedError()

    def run(self, cloud, box):
        raise NotImplementedError()

    def needs_confirm(self):
        return False


def add_node_command(cls):
    node_commands.append(cls())


def load_commands():
    # TODO: also search configured third-party dirs
    command_dirs = [
        # builtin_commands_dir
        os.path.dirname(__file__) + "/commands",
    ]
    if 'custom_command_dirs' in config.config:
        custom_command_dirs = config.config['custom_command_dirs']
        command_dirs.extend(custom_command_dirs)

    for path in command_dirs:
        load_commands_from_dir(path)


def load_commands_from_dir(path):
    modules = get_scripts_in_dir(path)
    # FIXME: Sketchy move to take precedence over global packages.  Better if
    # we don't touch the path and import by path.
    sys.path.insert(0, path)

    for module in modules:
        importlib.import_module(module)


def get_scripts_in_dir(path):
    assert os.path.exists(path)

    for file_name in os.listdir(path):
        if re.match(r'^[_.]', file_name):
            continue

        module = file_name[:-3]
        yield module
