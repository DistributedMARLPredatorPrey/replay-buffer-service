from dataclasses import dataclass


@dataclass(frozen=True)
class ReplayBufferConfig:
    """
    Sum type modelling the replay buffer configuration.
    """

    num_predators: int
    num_preys: int
    num_states: int
    dataset_path: str
