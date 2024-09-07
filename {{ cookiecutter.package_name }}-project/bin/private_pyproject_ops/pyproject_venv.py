# -*- coding: utf-8 -*-

"""
Virtualenv management related automation.
"""

import typing as T
import shutil
import subprocess
import dataclasses

from .helpers import print_command

if T.TYPE_CHECKING:  # pragma: no cover
    from .pyproject import PyProjectOps


@dataclasses.dataclass
class PyProjectVenv:
    """
    Namespace class for Virtualenv management related automation.

    :param python_version: example "3.7", "3.8", ...
    """

    python_version: str = dataclasses.field()

    def _validate_python_version(self: "PyProjectOps"):
        value_error = ValueError(
            f"'python_version' has to be in format of '3.7', '3.8', ..."
        )
        if self.python_version[0] not in ["3"]:
            raise value_error
        if self.python_version[1] != ".":
            raise value_error
        if not self.python_version[2:].isdigit():
            raise value_error
        if int(self.python_version[2:]) < 7:
            raise ValueError("python_version has to be >= 3.7")

    def _create_virtualenv(
        self: "PyProjectOps",
        dry_run: bool = False,
    ) -> bool:
        """
        Run:

        .. code-block:: bash

            $ virtualenv -p python${X}.${Y} ./.venv

        :return: a boolean flat to indicate whether a creation is performed.
        """
        if self.dir_venv.exists():
            return False
        else:
            args = [
                f"{self.path_bin_virtualenv}",
                "-p",
                f"python{self.python_version}",
                f"{self.dir_venv}",
            ]
            print_command(args)
            if dry_run is True:
                return False
            subprocess.run(args, check=True)
            return True

    def create_virtualenv(
        self: "PyProjectOps",
        dry_run: bool = False,
        verbose: bool = False,
    ) -> bool:  # pragma: no cover
        if verbose:
            flag = self._create_virtualenv(dry_run=dry_run)
            if flag:
                print("done")
            else:
                print(f"{self.dir_venv} already exists, do nothing.")
            return flag
        else:
            return self._create_virtualenv(dry_run=dry_run)

    def _remove_virtualenv(
        self: "PyProjectOps",
        dry_run: bool = False,
    ) -> bool:
        """
        Run:

        .. code-block:: bash

            $ rm -r /path/to/.venv

        :return: a boolean flat to indicate whether a deletion is performed.
        """
        if self.dir_venv.exists():
            print(f"run command: rm -r {self.dir_venv}")
            if dry_run is False:
                shutil.rmtree(f"{self.dir_venv}", ignore_errors=True)
            return True
        else:
            return False

    def remove_virtualenv(
        self: "PyProjectOps",
        dry_run: bool = False,
        verbose: bool = False,
    ):  # pragma: no cover
        if verbose:
            flag = self._remove_virtualenv(dry_run=dry_run)
            if flag:
                print(f"done! {self.dir_venv} is removed.")
            else:
                print(f"{self.dir_venv} doesn't exists, do nothing.")
            return flag
        else:
            return self._remove_virtualenv(dry_run=dry_run)