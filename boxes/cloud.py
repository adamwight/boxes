from libcloud.compute.types import NodeState
from libcloud.compute.providers import get_driver
import operator
import tabulate

from . import config

BASE_IMAGE = "debian-9-x64"
SIZE_MINIMUM = "1gb"
SIZE_BIGGER = "2gb"


class Cloud(object):
    def __init__(self):
        # TODO: We're actually coupled to DigitalOcean v2, so allowing
        # configurability is a ruse.
        cls = get_driver(config.config["cloud_driver"])
        self.driver = cls(config.config["api_token"], api_version="v2")

    def fetch(self):
        self.list = self.driver.list_nodes()
        self.list.sort(key=operator.attrgetter("name"))

    def list_all(self):
        data = []
        for i, box in enumerate(self.list):
            # FIXME: DO driver should extract size info out of extra.
            data.append([
                i,
                box.name,
                box.extra["memory"],
                box.extra["vcpus"],
                box.state,
            ])

        table = tabulate.tabulate(data, headers=[
            '',
            'name',
            'memory',
            'cpus',
            'status',
        ])
        return table

    def info(self, box):
        nets = box.extra['networks']['v4']
        ip = None
        for net in nets:
            if net['type'] == 'public':
                ip = net['ip_address']
                break

        info = [
            ['name', box.name],
            ['IPv4', ip],
            ['id', box.id],
            ['size', box.extra['size_slug']],
        ]
        return tabulate.tabulate(info)

    def resize(self, box, size):
        # Requires XXX PR
        assert box.extra['size_slug'] != size
        assert box.state == NodeState.STOPPED
        return self.driver.ex_resize_node(box, size)

    def rebuild(self, box):
        # Requires XXX PR
        return self.driver.ex_rebuild_node(box)

    def power_on(self, box):
        assert box.state == NodeState.STOPPED
        return self.driver.ex_power_on_node(box)

    def power_off(self, box):
        assert box.state == NodeState.RUNNING
        return self.driver.ex_shutdown_node(box)
