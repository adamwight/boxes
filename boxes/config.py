from yamlconfig import YamlConfig

config = {}


def load():
    global config
    config = YamlConfig("/etc/boxes.yaml")
