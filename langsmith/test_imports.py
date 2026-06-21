import subprocess
import sys


def test_langsmith_demo_imports_without_numpy_warning():
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import langsmith_demo; import metrics_dashboard; import test_scenarios",
        ],
        capture_output=True,
        text=True,
        cwd=str(__import__("pathlib").Path(__file__).resolve().parent),
        check=False,
    )
    combined = f"{result.stdout}\n{result.stderr}"
    assert result.returncode == 0, combined
    assert "NumPy 1.x cannot be run in NumPy 2" not in combined
