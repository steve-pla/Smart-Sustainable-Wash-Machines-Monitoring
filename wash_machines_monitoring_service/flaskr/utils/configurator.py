import yaml

def read_config(filename):
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config