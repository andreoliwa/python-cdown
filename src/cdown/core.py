from __future__ import annotations

import subprocess
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import List
from typing import Optional

from gitignore_parser import IgnoreRule
from gitignore_parser import rule_from_pattern

from cdown.exceptions import CodeOwnerFileNotFoundError


@dataclass
class CodeOwnerEntry:
    pattern: str
    owners: List[str]
    rule: IgnoreRule


class CodeOwnersFile:
    """File with the code owners patterns.

    Possible locations for the file:

    - root;
    - ``docs/`` directory;
    - ``.github/`` or ``.gitlab/`` directories.

    See the docs on:
    - `GitHub <https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/about-code-owners>`_
    - `GitLab <https://docs.gitlab.com/ee/user/project/code_owners.html>`_.
    """

    NAME = "CODEOWNERS"
    POSSIBLE_DIRECTORIES = ("", "docs", ".github", ".gitlab")

    def __init__(self, project_root: Path = None) -> None:
        self.entries: List[CodeOwnerEntry] = []
        self.project_root = project_root or Path.cwd()
        self._full_path: Optional[Path] = None

    @property
    def full_path(self) -> Path:
        return self._full_path

    def find(self) -> CodeOwnersFile:
        all_paths = []
        for possible_dir in self.POSSIBLE_DIRECTORIES:
            path = self.project_root / possible_dir / self.NAME
            if path.exists():
                self._full_path = path
                return self
            all_paths.append(str(path))

        bullet_list = "\n- ".join(all_paths)
        raise CodeOwnerFileNotFoundError(f"Code owners file not found in:\n- {bullet_list}")

    @lru_cache()
    def parse(self):
        """Parse a CODEOWNERS file (similar to a .gitignore file).

        Reusing ideas from ``gitignore_parser.parse_gitignore()``.
        """
        self.find()

        self.entries = []
        counter = 0
        for raw_line in reversed(self.full_path.read_text().splitlines()):
            pieces = [piece for piece in raw_line.split(" ") if piece]
            if len(pieces) < 2:
                continue

            pattern = pieces[0]
            owners = pieces[1:]

            counter += 1
            rule = rule_from_pattern(pattern, base_path=self.full_path.parent, source=(self.full_path, counter))
            if rule:
                self.entries.append(CodeOwnerEntry(pattern, owners, rule))

    def list_owners(self) -> List[str]:
        self.parse()
        owners = set()
        for entry in self.entries:
            for owner in entry.owners:
                owners.add(owner)
        return sorted(owners)

    def list_files(self):
        self.parse()
        return self.git_ls_files()

    def git_ls_files(self) -> List[str]:
        return (  # pragma: no cover
            subprocess.run(["git", "ls-files"], cwd=self.project_root, capture_output=True).stdout.decode().splitlines()
        )
