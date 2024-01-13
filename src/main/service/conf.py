import os
from typing import Dict

# Config data
conf: Dict[str, str] = {
    "REPLAY_BUFFER_PATH": f"{os.path.dirname(os.path.abspath(__file__))}/resources/data.csv"
}
