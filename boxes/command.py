"""
Framework for extensible actions
"""

import importlib
import os.path
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
    if not os.path.exists(path):
        raise RuntimeError("Bad custom command path: {}".format(path))

    sys.path.append(path)

    for module in os.listdir(path):
        if module == '__init__.py' or module[-3:] != '.py':
            continue
        importlib.import_module(module[:-3])
