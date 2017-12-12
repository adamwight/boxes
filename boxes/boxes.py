#!/usr/bin/env python

import curses
import re
import subprocess
import tabulate
import yaml

from doctl import doctl
from ui import ui


def gui_main(stdscr):
	w = ui(stdscr)

	d = doctl()
	d.fetch()
	table = d.list_all()
	w.print_block(table)

	# TODO: arrow/j/k selection, <ret> to open box
	index = int(w.prompt("Choose box: "))
	box = d.list[index]

	info = d.info(index=index)
	stdscr.clear()
	info += """
	(>) bigger -> {big}
	(<) smaller -> {small}
	(r)ebuild as {image}
	(p)uppet refresh
	(1) turn on
	(0) turn off""".format(big=SIZE_BIGGER, small=SIZE_MINIMUM, image=BASE_IMAGE)
	w.print_block(info)

	# TODO: add and provision box

	action = w.prompt("Operation? ")

	if action == '>':
		assert box['size']['slug'] == SIZE_MINIMUM
		assert box['status'] == 'off'
		out = doctl.resize(id=box['id'], size=SIZE_BIGGER)
		w.print_block(out)

	if action == '<':
		assert d.list[index]['size']['slug'] != SIZE_MINIMUM
		assert box['status'] == 'off'
		out = doctl.resize(id=box['id'], size=SIZE_MINIMUM)
		w.print_block(out)

	if action == 'r':
		confirm = w.prompt("Rebuild box {name}? (y/n) ".format(name=box['name']))
		assert confirm == 'y'
		out = doctl.rebuild(id=box['id'])
		w.print_block(out)

	if action == 'p':
		stdscr.clear()
		w.print_block("Refreshing puppet on " + box['name'])
		try:
			subprocess.check_output("./refresh_puppet.sh -l {name}".format(name=box['name']).split())
		except subprocess.CalledProcessError:
			# TODO: append text / to log
			w.print_block("Failed to jerk the puppet!")
			pass
		path = "/var/lib/puppet/state/last_run_report.yaml"
		local = "/tmp/last_run_report.yaml"
		subprocess.check_output("scp root@{name}:{path} {local}".format(name=box['name'], path=path, local=local).split())
		stdscr.clear()
		contents = open(local, "r").read()
		contents = re.sub(r'\s*!\S+', '', contents, flags=re.M)
		report = yaml.safe_load(contents)
		statuses = report['metrics']['resources']['values']
		statuses = [r[1:] for r in statuses]
		w.print_block(tabulate.tabulate(statuses))

	if action == '1':
		assert box['status'] == 'off'
		out = doctl.power_on(id=box['id'])
		w.print_block(out)

	if action == '0':
		assert box['status'] == 'active'
		out = doctl.power_off(id=box['id'])
		w.print_block(out)

	w.prompt("Any key to exit.")
	#stdscr.getkey()


def main():
    curses.wrapper(gui_main)
