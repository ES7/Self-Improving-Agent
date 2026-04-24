import os
from dotenv import load_dotenv

load_dotenv()

def _require(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(f"\n[Config Error] '{key}' not set.\n")
    return value

OPENAI_API_KEY: str = _require("OPENAI_API_KEY")
OPENAI_MODEL: str = "gpt-4o-mini"

# How many improvement iterations to run
MAX_ITERATIONS: int = 3

# Stop early if score reaches this threshold
TARGET_SCORE: int = 9
