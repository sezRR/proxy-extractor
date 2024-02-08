from configparser import ConfigParser, ExtendedInterpolation


class ConfigInitializer:
    def initialize_config(self) -> ConfigParser:
        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.read("config.ini")

        return config
