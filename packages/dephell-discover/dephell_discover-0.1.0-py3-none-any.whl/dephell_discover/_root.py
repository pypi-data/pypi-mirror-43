from itertools import chain
from pathlib import Path
from typing import List, Set, Optional

import attr

from ._constants import BAD_DIRS_ANY, BAD_DIRS_ROOT, BAD_EXTS
from ._cached_propery import cached_property
from ._package import Package
from ._data import Data


@attr.s()
class Root:
    path = attr.ib(type=Path)

    @property
    def name(self):
        return self.path.name

    def _make_data(self, path: Path, ext: str) -> Optional[Data]:
        paths = {package.path for package in self.packages}
        for parent in chain((path,), path.parents):
            if parent not in paths:
                continue
            return Data(path=path, ext=ext, package=Package(path=parent, root=self.path))
        # data not in any package
        return None

    def include(self, path: Path) -> bool:
        parts = path.parts[len(self.path.parts):]
        # hidden dirs and files in root dir
        if parts[0][0] == '.':
            return False
        # bad dirs in the root of the project
        if parts[0] in BAD_DIRS_ROOT:
            return False
        # bad dirs inside the project
        if set(parts) & BAD_DIRS_ANY:
            return False
        # bad extension
        if path.suffix.replace('.', '') in BAD_EXTS:
            return False
        return True

    @cached_property
    def packages(self) -> List[Package]:
        packages = []
        for path in self.path.glob('**/__init__.py'):
            if self.include(path=path):
                packages.append(Package(path=path.parent, root=self.path))
        return packages

    @cached_property
    def data(self) -> Set[Data]:
        result = set()
        for path in self.path.glob('**/*'):
            if not self.include(path=path):
                continue
            # skip dirs and python files
            if not path.is_file() or path.suffix == '.py':
                continue
            data = self._make_data(path=path.parent, ext=path.suffix)
            if data is not None:
                result.add(data)
        return result
