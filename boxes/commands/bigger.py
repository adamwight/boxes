from boxes.cloud import SIZE_BIGGER
from boxes.command import NodeCommand


class BiggerCommand(NodeCommand):
    def get_key(self):
        return ">"

    def get_description(self):
        return "(>) bigger -> {}".format(SIZE_BIGGER)

    def run(self, cloud, box):
        out = cloud.resize(box, SIZE_BIGGER)
        return "Success: {}".format(out)
