from boxes import command


class PowerOffCommand(command.NodeCommand):
    def get_key(self):
        return "0"

    def get_description(self):
        return "(0) turn off"

    def run(self, cloud, box):
        out = cloud.power_off(box)
        return "Success: {}".format(out)


command.add_node_command(PowerOffCommand)
