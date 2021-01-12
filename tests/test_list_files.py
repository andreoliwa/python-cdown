from functools import partial
from unittest import mock

from click.testing import CliRunner

from cdown import CodeOwnersFile
from cdown.cli import code_owners_cli


@mock.patch.object(CodeOwnersFile, "git_ls_files", return_value=["apps/inner.js", "root.js", "Makefile"])
def test_all_files_and_cli(git_ls_files, github_example):
    expected = [
        "@octocat                       apps/inner.js",
        "@js-owner                      root.js",
        "@global-owner1 @global-owner2  Makefile",
    ]

    assert list(CodeOwnersFile(github_example).list_files()) == expected

    result = CliRunner().invoke(code_owners_cli, ["--project", str(github_example), "ls-files"])
    assert result.output.splitlines() == expected
    assert result.exit_code == 0


@mock.patch.object(
    CodeOwnersFile,
    "git_ls_files",
    return_value=["apps/inner.js", "root.js", "Makefile", "here-we.go", "build/logs/sys/boot.log"],
)
def test_filter_files(git_ls_files, github_example):
    expected = [
        "@js-owner                      root.js",
        "docs@example.com               here-we.go",
        "@doctocat                      build/logs/sys/boot.log",
    ]
    list_files_generator = partial(CodeOwnersFile(github_example).list_files)
    assert list(list_files_generator("ot", "we")) == expected
    assert list(list_files_generator("we", "ot")) == expected

    result = CliRunner().invoke(code_owners_cli, ["--project", str(github_example), "ls-files", "we", "ot"])
    assert result.output.splitlines() == expected
    assert result.exit_code == 0
