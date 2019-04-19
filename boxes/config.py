import os.path
from yamlconfig import YamlConfig

search_path = ["boxes.yaml", "/etc/boxes.yaml"]
config = {}


def load():
    global config
    for path in search_path:
        path = os.path.abspath(os.path.expanduser(path))
        if os.path.exists(path):
            config = YamlConfig(path)
            return
    raise RuntimeError("No configs found in search path: " + str(search_path))
