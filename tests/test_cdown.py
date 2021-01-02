from pathlib import Path

import pytest
from click.testing import CliRunner

from cdown import CodeOwnersFile
from cdown.cli import list_owners


def test_code_owners_file_not_found(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        CodeOwnersFile(tmp_path).find()


@pytest.mark.parametrize("vcs_dir", CodeOwnersFile.POSSIBLE_DIRECTORIES)
def test_code_owners_file_found(vcs_dir, tmp_path: Path):
    file = tmp_path / vcs_dir / CodeOwnersFile.NAME
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text("")
    assert CodeOwnersFile(tmp_path).find().full_path == file


def test_simple_file_with_comments():  # FIXME[AA]:
    """Plus blank line, root dir and wildcard pattern."""
    pass


def test_list_owners_file_not_found():
    result = CliRunner().invoke(list_owners, [])
    assert result.output == f"{CodeOwnersFile.NAME} not found\n"
    assert result.exit_code == 1


def test_list_owners():  # FIXME[AA]:
    pass
