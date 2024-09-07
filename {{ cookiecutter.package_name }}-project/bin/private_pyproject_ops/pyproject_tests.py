# -*- coding: utf-8 -*-

"""
Testing related automation.
"""

import typing as T
import subprocess
import dataclasses

from .vendor.os_platform import OPEN_COMMAND
from .vendor.better_pathlib import temp_cwd

from .helpers import print_command

if T.TYPE_CHECKING:  # pragma: no cover
    from .pyproject import PyProjectOps


@dataclasses.dataclass
class PyProjectTests:
    """
    Namespace class for testing related automation.
    """

    def run_unit_test(
        self: "PyProjectOps",
        dry_run: bool = False,
    ):
        """
        A wrapper of ``pytest`` command to run unit test.
        """
        args = [
            f"{self.path_venv_bin_pytest}",
            f"{self.dir_tests}",
            "-s",
            f"--rootdir={self.dir_project_root}",
        ]
        with temp_cwd(self.dir_project_root):
            print_command(args)
            if dry_run is False:
                subprocess.run(args, check=True)

    def run_cov_test(
        self: "PyProjectOps",
        dry_run: bool = False,
    ):
        """
        A wrapper of ``pytest`` command to run code coverage test.
        """
        args = [
            f"{self.path_venv_bin_pytest}",
            "-s",
            "--tb=native",
            f"--rootdir={self.dir_project_root}",
            f"--cov={self.package_name}",
            "--cov-report",
            "term-missing",
            "--cov-report",
            f"html:{self.dir_htmlcov}",
            f"{self.dir_tests}",
        ]
        with temp_cwd(self.dir_project_root):
            print_command(args)
            if dry_run is False:
                subprocess.run(args, check=True)

    def view_cov(
        self: "PyProjectOps",
        dry_run: bool = False,
    ):
        """
        View coverage test output html file locally in web browser.

        It is usually at the ``${dir_project_root}/htmlcov/index.html``
        """
        args = [OPEN_COMMAND, f"{self.path_htmlcov_index_html}"]
        if dry_run is False:
            subprocess.run(args)

    def run_int_test(
        self: "PyProjectOps",
        dry_run: bool = False,
    ):
        """
        A wrapper of ``pytest`` command to run integration test.
        """
        args = [
            f"{self.path_venv_bin_pytest}",
            f"{self.dir_tests_int}",
            "-s",
            f"--rootdir={self.dir_project_root}",
        ]
        with temp_cwd(self.dir_project_root):
            print_command(args)
            if dry_run is False:
                subprocess.run(args, check=True)
