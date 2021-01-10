from unittest import mock

from click.testing import CliRunner

from cdown import CodeOwnersFile
from cdown.cli import code_owners_cli


@mock.patch.object(CodeOwnersFile, "git_ls_files", return_value=["apps/inner.js", "root.js", "Makefile"])
def test_list_files(git_ls_files, github_example):
    expected = [
        "@octocat                       apps/inner.js",
        "@js-owner                      root.js",
        "@global-owner1 @global-owner2  Makefile",
    ]

    assert list(CodeOwnersFile(github_example).list_files()) == expected

    result = CliRunner().invoke(code_owners_cli, ["--project", str(github_example), "ls-files"])
    assert result.output.splitlines() == expected
    assert result.exit_code == 0
