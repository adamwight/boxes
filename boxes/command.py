"""
Interface for node actions
"""
class NodeCommand(object):
    def get_key(self):
        raise NotImplementedError()

    def get_description(self):
        raise NotImplementedError()

    def run(self, cloud, box):
        raise NotImplementedError()
