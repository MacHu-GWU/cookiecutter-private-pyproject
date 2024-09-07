# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from pathlib import Path
from .vendor.jsonutils import json_loads
from .vendor.better_pathlib import get_dir_here

from .pyproject import PyProjectOps


@dataclasses.dataclass
class PyProjectOpsConfig:
    """
    ``pyproject_ops.json`` file stores the configuration for ``pyproject_ops`` CLI
    for your project.

    If you don't want to use the CLI, instead you want to use pyproject_ops
    as a Python library in your own automation script, you can create the
    :class:`PyProjectOps` object yourself.
    """

    package_name: str = dataclasses.field()
    dev_py_ver_major: int = dataclasses.field()
    dev_py_ver_minor: int = dataclasses.field()
    dev_py_ver_micro: int = dataclasses.field()
    aws_profile: str = dataclasses.field()
    aws_codeartifact_domain: str = dataclasses.field()
    aws_codeartifact_repository: str = dataclasses.field()
    doc_host_aws_profile: T.Optional[str] = dataclasses.field(default=None)
    doc_host_s3_bucket: T.Optional[str] = dataclasses.field(default=None)
    doc_host_s3_prefix: T.Optional[str] = dataclasses.field(default="projects/")


def find_pyproject_ops_json(dir_cwd: Path) -> Path:
    """
    Try to locate the ``pyproject_ops.json`` file by searching all the way up.
    """
    if dir_cwd.parent == dir_cwd:
        raise FileNotFoundError(
            f"Cannot find 'pyproject_ops.json' in {dir_cwd} or its parent directory."
        )
    path = dir_cwd.joinpath("private_pyproject_ops.json")
    if path.exists():
        return path
    else:
        return find_pyproject_ops_json(dir_cwd.parent)


dir_cwd = get_dir_here(__file__)
path_pyproject_ops_json = find_pyproject_ops_json(dir_cwd)
pyops_config = PyProjectOpsConfig(
    **json_loads(path_pyproject_ops_json.read_text(encoding="utf-8"))
)
pyops = PyProjectOps(
    dir_project_root=path_pyproject_ops_json.parent,
    package_name=pyops_config.package_name,
    python_version=f"{pyops_config.dev_py_ver_major}.{pyops_config.dev_py_ver_minor}",
    aws_profile=pyops_config.aws_profile,
    aws_codeartifact_domain=pyops_config.aws_codeartifact_domain,
    aws_codeartifact_repository=pyops_config.aws_codeartifact_repository,
    doc_host_s3_bucket=pyops_config.doc_host_s3_bucket,
)
