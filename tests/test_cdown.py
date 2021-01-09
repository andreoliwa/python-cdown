from pathlib import Path

import pytest
from click.testing import CliRunner

from cdown import CodeOwnersFile
from cdown.cli import list_owners
from cdown.cli import main
from cdown.exceptions import CodeOwnerFileNotFoundError


def test_code_owners_file_not_found(tmp_path: Path):
    with pytest.raises(CodeOwnerFileNotFoundError):
        CodeOwnersFile(tmp_path).find()


@pytest.mark.parametrize("vcs_dir", CodeOwnersFile.POSSIBLE_DIRECTORIES)
def test_code_owners_file_found(vcs_dir, tmp_path: Path):
    file = tmp_path / vcs_dir / CodeOwnersFile.NAME
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text("")
    assert CodeOwnersFile(tmp_path).find().full_path == file


@pytest.fixture()
def github_code_owners_example(tmp_path: Path) -> Path:
    """GitHub CODEOWNERS example.

    Taken from:
    https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/about-code-owners#example-of-a-codeowners-file
    """
    file_path = tmp_path / CodeOwnersFile.NAME
    file_path.write_text(
        """
        # This is a comment.
        # Each line is a file pattern followed by one or more owners.

        # These owners will be the default owners for everything in
        # the repo. Unless a later match takes precedence,
        # @global-owner1 and @global-owner2 will be requested for
        # review when someone opens a pull request.
        *       @global-owner1 @global-owner2

        # Order is important; the last matching pattern takes the most
        # precedence. When someone opens a pull request that only
        # modifies JS files, only @js-owner and not the global
        # owner(s) will be requested for a review.
        *.js    @js-owner

        # You can also use email addresses if you prefer. They'll be
        # used to look up users just like we do for commit author
        # emails.
        *.go docs@example.com

        # In this example, @doctocat owns any files in the build/logs
        # directory at the root of the repository and any of its
        # subdirectories.
        /build/logs/ @doctocat

        # The `docs/*` pattern will match files like
        # `docs/getting-started.md` but not further nested files like
        # `docs/build-app/troubleshooting.md`.
        docs/*  docs@example.com

        # In this example, @octocat owns any file in an apps directory
        # anywhere in your repository.
        apps/ @octocat

        # In this example, @doctocat owns any file in the `/docs`
        # directory in the root of your repository and any of its
        # subdirectories.
        /docs/ @doctocat
        """
    )
    return tmp_path


def test_list_owners_file_not_found():
    result = CliRunner().invoke(list_owners, [])
    assert "Error: Code owners file not found in" in result.output
    assert result.exit_code == 1


def test_list_owners(github_code_owners_example):
    result = CliRunner().invoke(
        main, ["--project", str(github_code_owners_example), "list-owners"]
    )
    assert result.output.splitlines() == [
        "@doctocat",
        "@global-owner1",
        "@global-owner2",
        "@js-owner",
        "@octocat",
        "docs@example.com",
    ]
    assert result.exit_code == 0
