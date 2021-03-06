from boxes import command


@command.node_command
class RebuildCommand(command.NodeCommand):
    def get_key(self):
        return "r"

    def get_description(self):
        return "(r)ebuild"

    def run(self, cloud, box, ui):
        out = cloud.rebuild(box)
        return "Success: {}".format(out)

    def needs_confirm(self):
        return True
