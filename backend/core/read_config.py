"""reads the config file"""
try:
    from ruamel.yaml import YAML
except ModuleNotFoundError:
    print("YAML module not found. Are you using `pipenv run`?")
    exit()


def get_real_path(file):
    """
    creates a path to file you are looking for
    kwargs:
    - file: (string) the file you want to create a path for
    """

    import os

    dir_path = os.path.dirname(os.path.realpath(__file__))
    abs_path = dir_path and os.path.join(dir_path, file)
    return abs_path


config_path = get_real_path("../config/config.yaml")
yaml = YAML(typ="safe")
stream = open(config_path, "r")
config = yaml.load(stream)
