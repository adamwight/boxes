#!/usr/bin/env python

import curses

from . import command
from . import config
from .cloud import Cloud
from .ui import ui


def gui_main(stdscr):
    curses = ui(stdscr)

    cloud = Cloud()
    cloud.fetch()
    table = cloud.list_all()
    curses.print_block(table)

    # TODO: arrow/j/k selection, <ret> to open box
    index = int(curses.prompt("Choose box: "))
    box = cloud.list[index]

    gui_box(curses, cloud, box)


def gui_box(curses, cloud, box):
    info = cloud.info(box)
    curses.clear()
    cmd_menu = get_all_commands()
    info += "\n" + "\n".join(cmd_menu)
    curses.print_block(info)

    action = curses.prompt("Operation? ")

    cmd = get_command_for_key(action)

    if cmd is None:
        raise RuntimeError("Unknown command key '{}'".format(action))

    out = cmd.run(cloud, box)
    curses.log_action(out)

    curses.prompt("Any key to exit.")


def get_all_commands():
    return [c.get_description() for c in command.node_commands]


def get_command_for_key(key):
    lookup = {c.get_key(): c for c in command.node_commands}

    if key in lookup:
        return lookup[key]

    return None


def main():
    config.load()
    command.load_commands()
    curses.wrapper(gui_main)
