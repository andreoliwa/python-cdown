from __future__ import annotations

import subprocess
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterator
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
        self.longest_owner_str = 0

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
        self.longest_owner_str = 0
        counter = 0
        for raw_line in reversed(self.full_path.read_text().splitlines()):
            pieces = [piece for piece in raw_line.split(" ") if piece]
            if len(pieces) < 2:
                continue

            pattern = pieces[0]
            owners = pieces[1:]

            counter += 1
            rule = rule_from_pattern(pattern, base_path=self.project_root, source=(self.full_path, counter))
            if rule:
                length = len(self.format_owners(owners))
                if self.longest_owner_str < length:
                    self.longest_owner_str = length
                self.entries.append(CodeOwnerEntry(pattern, owners, rule))

    @staticmethod
    def format_owners(owners: List[str]) -> str:
        return " ".join(owners)

    def list_owners(self) -> List[str]:
        self.parse()
        owners = set()
        for entry in self.entries:
            for owner in entry.owners:
                owners.add(owner)
        return sorted(owners)

    def list_files(self, *args: str) -> Iterator[str]:
        self.parse()

        filters = []
        if args:
            filters.extend(args)

        for relative_path in self.git_ls_files():
            include = not filters
            for part in filters:
                if part in relative_path:
                    include = True
                    break
            if not include:
                continue

            absolute_path = self.project_root / relative_path
            matched_entry = self.match(absolute_path)
            if matched_entry:
                yield f"{self.format_owners(matched_entry.owners):{self.longest_owner_str}}  {relative_path}"

    def git_ls_files(self) -> List[str]:
        """Return a list of relative paths of Git files in the project root."""
        return (  # pragma: no cover
            subprocess.run(["git", "ls-files"], cwd=self.project_root, capture_output=True).stdout.decode().splitlines()
        )

    def match(self, absolute_path: Path) -> Optional[CodeOwnerEntry]:
        """Match an entry to an absolute path.

        Exit on the first match: entries are reserved, later entries have higher priority.
        """
        for entry in self.entries:
            if entry.rule.match(absolute_path):
                return entry
        return None
