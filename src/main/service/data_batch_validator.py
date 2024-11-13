from src.main.parser.config import ReplayBufferConfig
from jsonschema import validate


class DataBatchValidator:
    """
    Data Batch Validator
    """

    def __init__(self, config: ReplayBufferConfig):
        self.__num_preds, self.__num_preys, self.__num_states, self.__num_actions = (
            config.num_predators,
            config.num_preys,
            config.num_states,
            config.num_actions,
        )

    def validate(self, data_batch):
        """
        Validates the data batch to have the required structure
        :param data_batch: Data batch to record
        :raise: ValidationError if not valid (check jsonschema documentation for details)
        """
        return validate(instance=data_batch, schema=self.__schema())

    def __schema(self):
        state_schema = {
            "type": "array",
            "items": {
                "type": "array",
                "minItems": self.__num_states * (self.__num_preds + self.__num_preys),
                "maxItems": self.__num_states * (self.__num_preds + self.__num_preys),
                "items": {"type": "number"},
            },
        }
        return {
            "type": "object",
            "properties": {
                "State": state_schema,
                "Reward": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "minItems": self.__num_preds + self.__num_preys,
                        "maxItems": self.__num_preds + self.__num_preys,
                        "items": {"type": "number"},
                    },
                },
                "Action": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "minItems": self.__num_actions
                        * (self.__num_preds + self.__num_preys),
                        "maxItems": self.__num_actions
                        * (self.__num_preds + self.__num_preys),
                        "items": {"type": "number"},
                    },
                },
                "Next State": state_schema,
            },
        }
