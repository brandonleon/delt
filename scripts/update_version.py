import re
import tomllib
from pathlib import Path

pyproject = Path("pyproject.toml").read_text()
version = tomllib.loads(pyproject)["project"]["version"]

init_file = Path("delt/__init__.py")
contents = init_file.read_text()
# Replace the version line in the docstring
new_contents = re.sub(
    r"(Current version:\s*)(\d+\.\d+\.\d+)",
    rf"\g<1>{version}",
    contents,
)
init_file.write_text(new_contents)
