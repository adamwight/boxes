from boxes.cloud import SIZE_MINIMUM
from boxes import command


@command.node_command
class SmallerCommand(command.NodeCommand):
    def get_key(self):
        return "<"

    def get_description(self):
        return "(<) smaller -> {}".format(SIZE_MINIMUM)

    def run(self, cloud, box, ui):
        out = cloud.resize(box, SIZE_MINIMUM)
        return "Resize {} smaller: {}".format(box.name, out)
