import os
import pytest
from agent.llm_factory import get_llm
def test_no_llm_key_raise_error():
    os.environ.pop("OPENAI_API_KEY",None)
    os.environ.pop("GROQ_API_KEY",None)
    with pytest.raises(RuntimeError):
        get_llm()