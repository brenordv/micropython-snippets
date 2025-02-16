from lib.config_manager import ConfigManager

config_manager = ConfigManager()

values_to_get = [
    "this_file",
    "some_number",
    "some_string",
    "some_boolean",
    "some_array",
    "some_object"
]

for value in values_to_get:
    print(f"{value}: {config_manager.get_value(value)}")
