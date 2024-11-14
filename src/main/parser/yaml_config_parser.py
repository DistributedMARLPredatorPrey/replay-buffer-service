import os
import yaml

from src.main.parser.config import ReplayBufferConfig


class YamlConfigParser:
    @staticmethod
    def __load_config(file_path):
        """
        Loads a config file.
        :param file_path: file's path
        :return: file's content
        """
        with open(file_path, "r") as conf:
            return yaml.safe_load(conf)

    def replay_buffer_configuration(self) -> ReplayBufferConfig:
        """
        Creates an ReplayBufferConfig object by extracting information from the config file,
        whose path is specified by GLOBAL_CONFIG_PATH environment variable.
        It also leverages environment variables.
        :return: environment config
        """
        env_conf = self.__load_config(os.environ.get("GLOBAL_CONFIG_PATH"))[
            "environment"
        ]
        return ReplayBufferConfig(
            num_predators=env_conf["num_predators"],
            num_preys=env_conf["num_preys"],
            num_states=env_conf["num_states"],
            dataset_path=os.environ.get("DATASET_PATH"),
        )
