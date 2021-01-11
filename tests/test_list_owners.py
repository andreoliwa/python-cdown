from click.testing import CliRunner

from cdown.cli import code_owners_cli


def test_cli_sorted_owners(github_example):
    result = CliRunner().invoke(code_owners_cli, ["--project", str(github_example), "ls-owners"])
    assert result.output.splitlines() == [
        "@doctocat",
        "@global-owner1",
        "@global-owner2",
        "@js-owner",
        "@octocat",
        "docs@example.com",
    ]
    assert result.exit_code == 0
