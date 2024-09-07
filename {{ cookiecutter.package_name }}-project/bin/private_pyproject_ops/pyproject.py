# -*- coding: utf-8 -*-

import dataclasses

from .pyproject_paths import PyProjectPaths
from .pyproject_venv import PyProjectVenv
from .pyproject_bsm import PyProjectBsm
from .pyproject_codeartifact import PyProjectCodeArtifact
from .pyproject_deps import PyProjectDeps
from .pyproject_tests import PyProjectTests
from .pyproject_docs import PyProjectDocs


@dataclasses.dataclass
class PyProjectOps(
    PyProjectPaths,
    PyProjectVenv,
    PyProjectBsm,
    PyProjectCodeArtifact,
    PyProjectDeps,
    PyProjectTests,
    PyProjectDocs,
):
    def __post_init__(self):
        self._validate_paths()
        self._validate_python_version()
