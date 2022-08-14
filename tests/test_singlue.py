from singlue import __version__
import pytest
import ast
from singlue import main
import subprocess
from pathlib import Path


def test_version():
    assert __version__ == "0.1.4"


@pytest.mark.parametrize(
    "resource_file_path",
    [
        "test_resources/example1.py",
        "test_resources/example2.py",
        "test_resources/example3.py",
        "test_resources/use_library_use_import.py",
        "test_resources/use_import_in_main.py",
    ],
)
def test_generated_files_finish_with_no_error(capsys, resource_file_path: str):
    source = Path(__file__).parent / resource_file_path
    with open(source) as f:
        res = ast.parse(source=f.read())
        main.run(res, str(source))
    captured_stdout: str = capsys.readouterr().out
    temp_file_path = Path(__file__).parent / "test_resources/temp.py"
    with open(temp_file_path, "w") as f:
        f.write(captured_stdout)

    assert subprocess.run(["python", temp_file_path]).returncode == 0

    temp_file_path.unlink()
