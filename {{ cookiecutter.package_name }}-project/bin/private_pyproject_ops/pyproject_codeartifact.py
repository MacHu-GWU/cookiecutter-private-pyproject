# -*- coding: utf-8 -*-

import typing as T
import dataclasses
import os
import shutil
import subprocess
from functools import cached_property

import botocore.exceptions
from .vendor.better_pathlib import temp_cwd

from .runtime import IS_CI
from .helpers import print_command

if T.TYPE_CHECKING:  # pragma: no cover
    from .pyproject import PyProjectOps


@dataclasses.dataclass
class PyProjectCodeArtifact:
    aws_codeartifact_domain: str = dataclasses.field()
    aws_codeartifact_repository: str = dataclasses.field()

    @property
    def poetry_secondary_source_name(self) -> str:
        return self.aws_codeartifact_repository.replace("-", "_")

    @cached_property
    def codeartifact_repository_endpoint(self: "PyProjectOps") -> str:
        """
        reference:

        - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/client/get_authorization_token.html
        """
        res = self.bsm.codeartifact_client.get_repository_endpoint(
            domain=self.aws_codeartifact_domain,
            repository=self.aws_codeartifact_repository,
            format="pypi",
        )
        return res["repositoryEndpoint"]

    @cached_property
    def codeartifact_authorization_token(self: "PyProjectOps") -> str:
        """
        reference:

        - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeartifact/client/get_authorization_token.html
        """
        res = self.bsm.codeartifact_client.get_authorization_token(
            domain=self.aws_codeartifact_domain,
        )
        return res["authorizationToken"]

    def poetry_source_add_codeartifact(self: "PyProjectOps"):
        """
        Run:

        .. code-block:: bash

            poetry source add --secondary ${source_name} "https://${domain_name}-${aws_account_id}.d.codeartifact.${aws_region}.amazonaws.com/pypi/${repository_name}/simple/"
        """
        endpoint = self.codeartifact_repository_endpoint
        args = [
            f"{self.path_bin_poetry}",
            "source",
            "add",
            "--priority=supplemental",
            self.poetry_secondary_source_name,
            f"{endpoint}simple/",
        ]
        print_command(args)
        subprocess.run(args, check=True)

    def poetry_authorization(self: "PyProjectOps"):
        """
        Set environment variables to allow Poetry to authenticate with CodeArtifact.
        """
        token = self.codeartifact_authorization_token
        source_name = self.poetry_secondary_source_name.upper()
        os.environ[f"POETRY_HTTP_BASIC_{source_name}_USERNAME"] = "aws"
        os.environ[f"POETRY_HTTP_BASIC_{source_name}_PASSWORD"] = token

    def twine_authorization(self: "PyProjectOps"):
        """
        Run

        .. code-block:: bash

            aws codeartifact login --tool twine \
                --domain ${domain_name} \
                --domain-owner ${aws_account_id} \
                --repository ${repo_name} \
                --profile ${aws_profile}

        Reference:

        - `Configure and use twine with CodeArtifact <https://docs.aws.amazon.com/codeartifact/latest/ug/python-configure-twine.html>`_
        - `AWS CodeArtifact CLI <https://docs.aws.amazon.com/cli/latest/reference/codeartifact/index.html>`_
        """
        args = [
            f"{self.path_bin_aws}",
            "codeartifact",
            "login",
            "--tool",
            "twine",
            "--domain",
            self.aws_codeartifact_domain,
            "--domain-owner",
            self.bsm.aws_account_id,
            "--repository",
            self.aws_codeartifact_repository,
        ]
        if IS_CI is False:
            if self.bsm.profile_name:
                args.extend(["--profile", self.bsm.profile_name])

        print_command(args)
        subprocess.run(args, check=True)

    def twine_upload(self: "PyProjectOps"):
        """
        Upload Python package to CodeArtifact.

        Run

        .. code-block:: bash

            twine upload dist/* --repository codeartifact
        """
        console_url = (
            f"https://{self.bsm.aws_region}.console.aws.amazon.com/codesuite/codeartifact/d"
            f"/{self.bsm.aws_account_id}/{self.aws_codeartifact_domain}/r"
            f"/{self.aws_codeartifact_repository}/p/pypi/"
            f"{self.package_name}/versions?region={self.bsm.aws_region}"
        )
        print(f"preview in AWS CodeArtifact console: {console_url}")
        self.twine_authorization()
        args = ["twine", "upload", f"{self.dir_dist}/*", "--repository", "codeartifact"]
        print_command(args)
        with temp_cwd(self.dir_project_root):
            subprocess.run(args, check=True)

    def poetry_build(self: "PyProjectOps"):
        shutil.rmtree(self.dir_dist, ignore_errors=True)
        args = [
            f"{self.path_bin_poetry}",
            "build",
        ]
        print_command(args)
        with temp_cwd(self.dir_project_root):
            subprocess.run(args, check=True)

    def publish_to_codeartifact(self: "PyProjectOps"):
        """
        Publish your Python package to AWS CodeArtifact
        """
        try:
            res = self.bsm.codeartifact_client.describe_package_version(
                domain=self.aws_codeartifact_domain,
                repository=self.aws_codeartifact_repository,
                format="pypi",
                package=self.normalized_package_name,
                packageVersion=self.package_version,
            )
            message = (
                f"package {self.normalized_package_name!r} "
                f"= {self.package_version} already exists!"
            )
            raise Exception(message)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                pass
            else:
                raise e

        self.poetry_build()
        self.twine_upload()

    def remove_from_codeartifact(self: "PyProjectOps"):
        """
        Publish your Python package to AWS CodeArtifact
        """
        # try:
        res = input(
            f"Are you sure you want to remove the package {self.normalized_package_name!r} "
            f"version {self.package_version!r}? (Y/N): "
        )
        if res == "Y":
            res = self.bsm.codeartifact_client.delete_package_versions(
                domain=self.aws_codeartifact_domain,
                repository=self.aws_codeartifact_repository,
                format="pypi",
                package=self.normalized_package_name,
                versions=[self.package_version],
                expectedStatus="Published",
            )
            print("Package version removed.")
        else:
            print("Aborted")
