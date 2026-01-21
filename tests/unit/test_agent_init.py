import os
import pytest
from agent.agent import create_agent


def test_agent_fails_without_api_key():
    os.environ.pop("OPENAI_API_KEY",None)
    with pytest.raises(RuntimeError):
        create_agent()
def func():
    pass
