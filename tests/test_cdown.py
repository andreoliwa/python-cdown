from click.testing import CliRunner

from cdown.cli import list_owners


def test_code_owners_file_not_found():  # FIXME[AA]:
    pass


def test_github_code_owners_file_found():  # FIXME[AA]:
    pass


def test_gitlab_code_owners_file_found():  # FIXME[AA]:
    pass


def test_simple_file_with_comments():  # FIXME[AA]:
    """Plus blank line, root dir and wildcard pattern."""
    pass


def test_list_owners():  # FIXME[AA]:
    runner = CliRunner()
    result = runner.invoke(list_owners, [])

    assert result.output == ""
    assert result.exit_code == 0
