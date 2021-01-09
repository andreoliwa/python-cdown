from unittest import mock

from click.testing import CliRunner

from cdown import CodeOwnersFile
from cdown.cli import code_owners_cli


@mock.patch.object(CodeOwnersFile, "git_ls_files")
def test_cli_all_files(git_ls_files, github_example):
    git_ls_files.return_value = ["a", "b", "c"]
    result = CliRunner().invoke(code_owners_cli, ["--project", str(github_example), "ls-files"])
    assert result.output.splitlines() == git_ls_files.return_value
    assert result.exit_code == 0
