import ujson

class ConfigManager:
    def __init__(self, config_file= "appsettings.json"):
        self.config_file = config_file
        self.config = {}
        self.load_config()

    def load_config(self):
        with open(self.config_file, "r", encoding="utf-8") as f:
            self.config = ujson.loads(f.read())

    def get_value(self, key, default_value=None):
        return self.config.get(key, default_value)
