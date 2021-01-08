from __future__ import annotations

__version__ = "0.0.0"

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import List
from typing import Optional

from gitignore_parser import IgnoreRule

from cdown.exceptions import CodeOwnerFileNotFoundError


@dataclass
class CodeOwnerEntry:
    pattern: str
    #: An owner in the format: @company/[namespace]/team
    owner: str

    _rule: IgnoreRule

    @property
    def company(self) -> str:
        return ""  # FIXME[AA]:

    @property
    def namespace(self) -> str:
        return ""  # FIXME[AA]:

    @property
    def team(self) -> str:
        return ""  # FIXME[AA]:


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

    def __init__(self, project_root: Path = None, file_path: Path = None) -> None:
        self.entries: List[CodeOwnerEntry] = []
        self.project_root = project_root or Path.cwd()
        self._full_path: Optional[Path] = file_path or None

    @property
    def full_path(self) -> Path:
        return self._full_path

    def find(self) -> CodeOwnersFile:
        if self._full_path:
            return self
        all_paths = []
        for possible_dir in self.POSSIBLE_DIRECTORIES:
            path = self.project_root / possible_dir / self.NAME
            if path.exists():
                self._full_path = path
                return self
            all_paths.append(str(path))

        bullet_list = "\n- ".join(all_paths)
        raise CodeOwnerFileNotFoundError(
            f"Code owners file not found in:\n- {bullet_list}"
        )

    @lru_cache()
    def parse(self):
        self.find()

    def list_owners(self) -> List[str]:
        self.parse()
        return sorted({entry.owner for entry in self.entries})
