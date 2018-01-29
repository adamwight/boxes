from boxes import command


@command.node_command
class PowerOffCommand(command.NodeCommand):
    def get_key(self):
        return "0"

    def get_description(self):
        return "(0) turn off"

    def run(self, cloud, box, ui):
        out = cloud.power_off(box)
        return "Success: {}".format(out)
