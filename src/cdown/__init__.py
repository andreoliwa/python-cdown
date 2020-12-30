__version__ = "0.0.0"

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import List

from gitignore_parser import IgnoreRule


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
    def __init__(self, project_root: Path = None) -> None:
        self.entries: List[CodeOwnerEntry] = []
        self.project_root = project_root or Path.cwd()

    @lru_cache()
    def parse(self):
        self.find()

    def find(self):
        # FIXME[AA]: search GitHub CODEOWNERS
        # FIXME[AA]: search GitLab CODEOWNERS
        pass

    def list_owners(self) -> List[str]:
        self.parse()
        return sorted({entry.owner for entry in self.entries})
