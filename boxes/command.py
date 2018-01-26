"""
Framework for extensible actions
"""

import importlib
import os.path
import sys

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
    commands_dir = os.path.dirname(__file__) + "/commands"
    sys.path.append(commands_dir)

    for module in os.listdir(commands_dir):
        if module == '__init__.py' or module[-3:] != '.py':
            continue
        importlib.import_module(module[:-3])
