#!/usr/bin/env python

import curses
import re
import subprocess
import tabulate
import yaml

from . import command
from . import config
from .cloud import Cloud, SIZE_BIGGER, SIZE_MINIMUM, BASE_IMAGE
from .ui import ui


def gui_main(stdscr):
    w = ui(stdscr)

    d = Cloud()
    d.fetch()
    table = d.list_all()
    w.print_block(table)

    # TODO: arrow/j/k selection, <ret> to open box
    index = int(w.prompt("Choose box: "))
    box = d.list[index]

    info = d.info(index=index)
    stdscr.clear()
    cmd_menu = [c.get_description() for c in command.node_commands]
    info += "\n" + "\n".join(cmd_menu)
    w.print_block(info)

    # TODO: add and provision box

    action = w.prompt("Operation? ")

    cmd_key_lookup = {c.get_key(): c for c in command.node_commands}

    if action in cmd_key_lookup:
        out = cmd_key_lookup[action].run(d, box)
        w.print_block(out)

    w.prompt("Any key to exit.")


def main():
    config.load()
    command.load_commands()
    curses.wrapper(gui_main)
