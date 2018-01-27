#!/usr/bin/env python

import curses

from . import command
from . import config
from .cloud import Cloud
from .ui import Ui


def gui_main(stdscr):
    ui = Ui(stdscr)

    cloud = Cloud()
    cloud.fetch()
    table = cloud.list_all()
    # TODO: menu entry for (*) cloud commands
    ui.print_block(table)

    # TODO: arrow/j/k selection, <ret> to open box
    index = int(ui.prompt("Choose box: "))
    box = cloud.list[index]

    gui_box(ui, cloud, box)


def gui_box(ui, cloud, box):
    info = cloud.info(box)
    ui.clear()
    cmd_menu = get_all_commands()
    info += "\n" + "\n".join(cmd_menu)
    ui.print_block(info)

    action = ui.prompt("Operation? ")

    cmd = get_command_for_key(action)

    if cmd is None:
        raise RuntimeError("Unknown command key '{}'".format(action))

    out = cmd.run(cloud, box, ui)
    ui.log_action(out)

    ui.prompt("Any key to exit.")


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
