from boxes.cloud import SIZE_BIGGER
from boxes import command


class BiggerCommand(command.NodeCommand):
    def get_key(self):
        return ">"

    def get_description(self):
        return "(>) bigger -> {}".format(SIZE_BIGGER)

    def run(self, cloud, box, ui):
        out = cloud.resize(box, SIZE_BIGGER)
        return "Resize {} bigger: {}".format(box.name, out)


command.add_node_command(BiggerCommand)
