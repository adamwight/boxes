import yaml

from boxes import command


@command.node_command
class ExtendedInfoCommand(command.NodeCommand):
    def get_key(self):
        return "i"

    def get_description(self):
        return "extended (i)nfo"

    def run(self, cloud, box, ui):
        # TODO: fancy this up
        out = yaml.dump(box.extra)
        return "Extended info:\n{}".format(out)
