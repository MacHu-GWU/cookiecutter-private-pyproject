# -*- coding: utf-8 -*-

"""
Documentation build an deploy related automation.
"""

import typing as T
import os
import shutil
import dataclasses
import subprocess

from .vendor.os_platform import OPEN_COMMAND

from .helpers import print_command

if T.TYPE_CHECKING:  # pragma: no cover
    from .pyproject import PyProjectOps


@dataclasses.dataclass
class PyProjectDocs:
    """
    Namespace class for document related automation.
    """

    doc_host_s3_bucket: str = dataclasses.field()

    def build_doc(
        self: "PyProjectOps",
        dry_run: bool = False,
    ):
        """
        Use sphinx doc to build documentation site locally. It set the
        necessary environment variables so that the ``make html`` command
        can build the HTML successfully.
        """
        if dry_run is False:
            shutil.rmtree(f"{self.dir_sphinx_doc_build}", ignore_errors=True)
            shutil.rmtree(
                f"{self.dir_sphinx_doc_source_python_lib}", ignore_errors=True
            )

        # this allows the ``make html`` command knows which python virtualenv to use
        # see more information at: https://docs.python.org/3/library/venv.html
        os.environ["PATH"] = (
            f"{self.dir_venv_bin}" + os.pathsep + os.environ.get("PATH", "")
        )
        os.environ["VIRTUAL_ENV"] = f"{self.dir_venv}"
        args = [
            "make",
            "-C",
            f"{self.dir_sphinx_doc}",
            "html",
        ]
        print_command(args)
        if dry_run is False:
            subprocess.run(args)

    def view_doc(
        self: "PyProjectOps",
        dry_run: bool = False,
    ):
        """
        View documentation site built locally in web browser.

        It is usually at the ``${dir_project_root}/build/html/index.html``
        """
        args = [OPEN_COMMAND, f"{self.path_sphinx_doc_build_index_html}"]
        print_command(args)
        if dry_run is False:
            subprocess.run(args)

    def deploy_versioned_doc(
        self: "PyProjectOps",
        prefix: str = "projects/",
        aws_profile: T.Optional[str] = None,
        dry_run: bool = False,
    ):
        """
        Deploy versioned document to AWS S3.

        The S3 bucket has to enable static website hosting. The document site
        will be uploaded to ``s3://${bucket}/${prefix}${package_name}/${package_version}/``
        """
        args = [
            f"{self.path_bin_aws}",
            "s3",
            "sync",
            f"{self.dir_sphinx_doc_build_html}",
            f"s3://{self.doc_host_s3_bucket}/{prefix}{self.package_name}/{self.package_version}/",
        ]
        if aws_profile:
            args.extend(["--profile", aws_profile])
        print_command(args)
        if dry_run is False:
            subprocess.run(args, check=True)

    def deploy_latest_doc(
        self: "PyProjectOps",
        prefix: str = "projects/",
        aws_profile: T.Optional[str] = None,
        dry_run: bool = False,
    ):
        """
        Deploy the latest document to AWS S3.

        The S3 bucket has to enable static website hosting. The document site
        will be uploaded to ``s3://${bucket}/${prefix}${package_name}/latest/``
        """
        args = [
            f"{self.path_bin_aws}",
            "s3",
            "sync",
            f"{self.dir_sphinx_doc_build_html}",
            f"s3://{self.doc_host_s3_bucket}/{prefix}{self.package_name}/latest/",
        ]
        if aws_profile:
            args.extend(["--profile", aws_profile])
        print_command(args)
        if dry_run is False:
            subprocess.run(args, check=True)

    def view_latest_doc(
        self: "PyProjectOps",
        prefix: str = "projects/",
        dry_run: bool = False,
    ):
        """
        Open the latest document that hosted on AWS S3 in web browser.

        Here's a sample document site url
        https://my-bucket.s3.amazonaws.com/my-prefix/my_package/latest/index.html
        """
        url = (
            f"https://{self.doc_host_s3_bucket}.s3.amazonaws.com/{prefix}{self.package_name}"
            f"/latest/{self.path_sphinx_doc_build_index_html.name}"
        )
        args = [OPEN_COMMAND, url]
        print_command(args)
        if dry_run is False:
            subprocess.run(args, check=True)
