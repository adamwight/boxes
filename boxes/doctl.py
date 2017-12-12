import json
import platform
import subprocess
import tabulate

BASE_IMAGE = "debian-9-x64"
SIZE_MINIMUM = "512mb"
SIZE_BIGGER = "2gb"


class doctl(object):
	def __init__(self):
		pass

	@staticmethod
	def run_command(args):
		if platform.system() == 'Darwin':
			cmd = "/usr/local/bin/doctl"
		else:
			cmd = "snap run doctl"

		cmd += " " + args
		out = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT)

		return out

	def fetch(self):
		out = doctl.run_command("compute droplet list -o json")
		self.list = json.loads(out)

	def list_all(self):
		data = []
		for i, box in enumerate(self.list):
			data.append([i, box['name'], box['memory'], box['vcpus'], box['status']])

		table = tabulate.tabulate(data, headers=['', 'name', 'memory', 'cpus', 'status'])
		return table

	def info(self, index=None):
		if index:
			box = self.list[index]

		nets = box['networks']['v4']
		ip = None
		for net in nets:
			if net['type'] == 'public':
				ip = net['ip_address']
				break

		info = [
			['name', box['name']],
			['IPv4', ip],
			['id', box['id']],
			['size', box['size']['slug']],
		]
		return tabulate.tabulate(info)

	@staticmethod
	def resize(id, size):
		return doctl.run_command("compute droplet-action resize {id} --size {size} --trace -v".format(id=id, size=size))

	@staticmethod
	def rebuild(id):
		return doctl.run_command("compute droplet-action rebuild {id} --wait --image {image}".format(id=id, image=BASE_IMAGE))

	@staticmethod
	def power_on(id):
		return doctl.run_command("compute droplet-action power-on {id}".format(id=id))

	@staticmethod
	def power_off(id):
		return doctl.run_command("compute droplet-action power-off {id}".format(id=id))
