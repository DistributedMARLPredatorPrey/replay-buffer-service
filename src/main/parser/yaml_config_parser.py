import os
import yaml

from src.main.parser.config import EnvironmentConfig, ReplayBufferConfig


class YamlConfigParser:

    @staticmethod
    def _load_config(env_var):
        with open(env_var, "r") as conf:
            return yaml.safe_load(conf)

    def environment_configuration(self):
        env_conf = self._load_config(os.environ.get("GLOBAL_CONFIG_PATH"))["environment"]
        return EnvironmentConfig(
            num_predators=env_conf["num_predators"],
            num_preys=env_conf["num_preys"],
            acc_lower_bound=env_conf["acc_lower_bound"],
            acc_upper_bound=env_conf["acc_upper_bound"],
            num_states=env_conf["num_states"],
            num_actions=env_conf["num_actions"],
        )

    def replay_buffer_configuration(self):
        return ReplayBufferConfig(
            predator_dataset_path=os.environ.get("PREDATOR_DATASET_PATH"),
            prey_dataset_path=os.environ.get("PREY_DATASET_PATH"),
        )
