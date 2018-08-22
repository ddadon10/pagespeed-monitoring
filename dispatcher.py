import yaml
import app


class _ConfigFile:
    def __init__(self, path):
        with open(path, "r") as stream:
            try:
                self.data = yaml.load(stream)
            except yaml.YAMLError as exc:
                raise exc


def handler(event, context):
    config_file = _ConfigFile('config.yml')
    config = config_file.data["websites"][event['website']]
    print(config)
    for el in config:
        app.handler({"config": el}, context)

# def test():
#     config = _ConfigFile('config.yml')
#     for website in config.config['websites'].values():
#         for page in website:
#             app.handler({'config': page}, None)
#
# test()