import re
import subprocess
import tabulate
import yaml

from boxes import command


# TODO: This is a custom command which can't be distributed with the FLOSS
# version.

class RefreshPupppetCommand(command.NodeCommand):
    def get_key(self):
        return "p"

    def get_description(self):
        return "(p)uppet refresh"

    def run(self, cloud, box):
        # TODO:
        # stdscr.clear()
        # w.print_block("Refreshing puppet on " + box['name'])
        try:
            subprocess.check_output(
                "./refresh_puppet.sh -l {}".format(box.name).split())
        except subprocess.CalledProcessError:
            # TODO: append text / to log
            return "Failed to jerk the puppet!"

        remote_path = "/var/lib/puppet/state/last_run_report.yaml"
        local_path = "/tmp/last_run_report.yaml"
        subprocess.check_output(
            "scp root@{name}:{path} {local}".format(
                name=box['name'],
                path=remote_path,
                local=local_path
            ).split())
        # TODO
        # stdscr.clear()
        with open(local_path, "r") as f:
            contents = f.read()
            contents = re.sub(r'\s*!\S+', '', contents, flags=re.M)
            report = yaml.safe_load(contents)
        statuses = report['metrics']['resources']['values']
        statuses = [r[1:] for r in statuses]
        return tabulate.tabulate(statuses)


command.add_node_command(RefreshPupppetCommand)
