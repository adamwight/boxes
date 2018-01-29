from boxes import command


@command.node_command
class PowerOnCommand(command.NodeCommand):
    def get_key(self):
        return "1"

    def get_description(self):
        return "(1) turn on"

    def run(self, cloud, box, ui):
        out = cloud.power_on(box)
        return "Success: {}".format(out)
