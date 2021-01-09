from pathlib import Path

import pytest
from click.testing import CliRunner

from cdown import CodeOwnersFile
from cdown.cli import ls_owners
from cdown.exceptions import CodeOwnerFileNotFoundError


def test_not_found(tmp_path: Path):
    with pytest.raises(CodeOwnerFileNotFoundError):
        CodeOwnersFile(tmp_path).find()


@pytest.mark.parametrize("vcs_dir", CodeOwnersFile.POSSIBLE_DIRECTORIES)
def test_found(vcs_dir, tmp_path: Path):
    file = tmp_path / vcs_dir / CodeOwnersFile.NAME
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text("")
    assert CodeOwnersFile(tmp_path).find().full_path == file


def test_cli_file_not_found():
    result = CliRunner().invoke(ls_owners, [])
    assert "Error: Code owners file not found in" in result.output
    assert result.exit_code == 1
