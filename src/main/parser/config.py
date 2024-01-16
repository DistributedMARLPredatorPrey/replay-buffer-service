from dataclasses import dataclass


@dataclass(frozen=True)
class EnvironmentConfig:
    num_predators: int
    num_preys: int
    acc_lower_bound: float
    acc_upper_bound: float
    num_states: int
    num_actions: int


@dataclass(frozen=True)
class ReplayBufferConfig:
    predator_dataset_path: str
    prey_dataset_path: str
