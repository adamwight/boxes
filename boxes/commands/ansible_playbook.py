import glob
import os.path
import subprocess

from boxes import command


playbooks = []


class AnsibleCommand(command.NodeCommand):
    def get_key(self):
        return "a"

    def get_description(self):
        return "Run an (a)nsible playbook"

    def run(self, cloud, box, ui):
        ui.clear()
        menu = "Ansible playbooks:\n"
        lookup = {}
        for index, playbook in enumerate(playbooks):
            key = chr(ord("a") + index)
            lookup[key] = playbook
            short_name = os.path.basename(playbook)[:-5]
            menu += "({}) {}\n".format(key, short_name)

        ui.print_block(menu)
        action = ui.prompt("Choose a playbook: ")
        assert action in lookup

        cmd = "ansible-playbook {} -l {}".format(lookup[action], box.name)
        out = subprocess.check_output(cmd.split())

        return "Ran {} on {}\n{}".format(lookup[action], box.name, out)


def scan_playbooks():
    global playbooks

    # TODO: make path configurable
    path = os.getcwd() + "/playbooks"
    if not os.path.exists(path):
        return

    for file_path in glob.glob(path + "/*.yaml"):
        playbooks.append(file_path)

    if not playbooks:
        return

    # TODO: Option to make the playbooks top-level commands.
    command.add_node_command(AnsibleCommand)


scan_playbooks()
