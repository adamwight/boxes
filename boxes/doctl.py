import json
from libcloud.compute.types import NodeState
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import platform
import subprocess
import tabulate

from . import config

BASE_IMAGE = "debian-9-x64"
SIZE_MINIMUM = "1gb"
SIZE_BIGGER = "2gb"


class doctl(object):
    def __init__(self):
        cls = get_driver(Provider.DIGITAL_OCEAN)
        self.driver = cls(config.config["api_token"], api_version="v2")

    def fetch(self):
        self.list = self.driver.list_nodes()

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

    def info(self, index=None):
        if index is None:
            return

        box = self.list[index]

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

    # FIXME: libcloud doesn't support resize
    #@staticmethod
    #def resize(id, size):
    #    return doctl.run_command("compute droplet-action resize {id} --size {size} --trace -v".format(id=id, size=size))

    # FIXME: libcloud doesn't support rebuild
    #@staticmethod
    #def rebuild(id):
    #    return doctl.run_command("compute droplet-action rebuild {id} --wait --image {image}".format(id=id, image=BASE_IMAGE))

    def power_on(self, box):
        assert box.state == NodeState.STOPPED
        return self.driver.ex_power_on_node(box)

    def power_off(self, box):
        assert box.state == NodeState.RUNNING
        return self.driver.ex_shutdown_node(box)
