import subprocess
import sys


def test_langchain_openai_import_without_numpy_compat_warning():
    """langchain_openai pulls transformers/torch; torch must match numpy major version."""
    result = subprocess.run(
        [sys.executable, "-W", "default", "-c", "from langchain_openai import ChatOpenAI"],
        capture_output=True,
        text=True,
        check=False,
    )
    combined = f"{result.stdout}\n{result.stderr}"
    assert "NumPy 1.x cannot be run in NumPy 2" not in combined
    assert "Failed to initialize NumPy" not in combined
