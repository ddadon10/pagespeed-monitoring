import yaml
import app


class _ConfigFile:
    def __init__(self, path):
        with open(path, "r") as stream:
            try:
                self.config = yaml.load(stream)
            except yaml.YAMLError as exc:
                raise exc


def handler(event, context):
    #config = _ConfigFile('config.yml')
    print(event)


# def test():
#     config = _ConfigFile('config.yml')
#     for website in config.config['websites'].values():
#         for page in website:
#             app.handler({'config': page}, None)
#
# test()