# -*- coding: utf-8 -*-

"""
Requirements::

    pip install "boto_session_manager>=1.7.2,<2.0.0"
    pip install "PyGithub>=2.1.1,<3.0.0"
"""

import json
from pathlib import Path

from github import Github
import botocore.exceptions
from boto_session_manager import BotoSesManager

# ------------------------------------------------------------------------------
# **Custom this**
# ------------------------------------------------------------------------------
github_username = "{{ cookiecutter.github_username }}"
repo_name = "{{ cookiecutter.package_name }}-project"
github_token_name = "{{ cookiecutter.github_token_name }}"
aws_profile = "{{ cookiecutter.aws_profile }}"
aws_codeartifact_domain = "{{ cookiecutter.aws_codeartifact_domain }}"  # make sure it match pyproject.toml
aws_codeartifact_repository = "{{ cookiecutter.aws_codeartifact_repository }}"  # make sure it match pyproject.toml

# ------------------------------------------------------------------------------
# Don't touch the code below
# ------------------------------------------------------------------------------
dir_home = Path.home()
dir_here = Path(__file__).absolute().parent
path_access_key_json = dir_here.joinpath("access_key-delete_me_soon.json")

iam_user_name = f"gh_ci-{repo_name}"
print(f"{iam_user_name = }")

bsm = BotoSesManager(profile_name=aws_profile)


def get_github_token_file(
    owner_username: str,
    token_name: str,
) -> Path:
    """
    Ref: https://dev-exp-share.readthedocs.io/en/latest/search.html?q=store-token-on-local-laptop&check_keywords=yes&area=default
    """
    return dir_home / ".github" / "pac" / owner_username / f"{token_name}.txt"


def main():
    # --- create user
    try:
        bsm.iam_client.create_user(UserName=iam_user_name)
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "EntityAlreadyExists":
            pass
        else:
            raise e

    # --- set iam policy
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "codeartifact:DescribeDomain",
                    "codeartifact:DescribePackage",
                    "codeartifact:DescribePackageGroup",
                    "codeartifact:DescribePackageVersion",
                    "codeartifact:DescribeRepository",
                    "codeartifact:GetAssociatedPackageGroup",
                    "codeartifact:GetAuthorizationToken",
                    "codeartifact:GetDomainPermissionsPolicy",
                    "codeartifact:GetPackageVersionAsset",
                    "codeartifact:GetPackageVersionReadme",
                    "codeartifact:GetRepositoryEndpoint",
                    "codeartifact:GetRepositoryPermissionsPolicy",
                    "codeartifact:ListAllowedRepositoriesForGroup",
                    "codeartifact:ListAssociatedPackages",
                    "codeartifact:ListPackageGroups",
                    "codeartifact:ListPackages",
                    "codeartifact:ListPackageVersionAssets",
                    "codeartifact:ListPackageVersionDependencies",
                    "codeartifact:ListPackageVersions",
                    "codeartifact:ListRepositoriesInDomain",
                    "codeartifact:ListSubPackageGroups",
                    "codeartifact:ListTagsForResource",
                    "codeartifact:ReadFromRepository",
                ],
                "Resource": [
                    f"arn:aws:codeartifact:{bsm.aws_region}:{bsm.aws_account_id}:domain/{aws_codeartifact_domain}",
                    f"arn:aws:codeartifact:{bsm.aws_region}:{bsm.aws_account_id}:repository/{aws_codeartifact_domain}/{aws_codeartifact_repository}",
                    f"arn:aws:codeartifact:{bsm.aws_region}:{bsm.aws_account_id}:package/{aws_codeartifact_domain}/*/*/*/*",
                    f"arn:aws:codeartifact:{bsm.aws_region}:{bsm.aws_account_id}:package-group/{aws_codeartifact_domain}*",
                ],
            },
            {
                "Sid": "VisualEditor1",
                "Effect": "Allow",
                "Action": ["codeartifact:ListRepositories", "codeartifact:ListDomains"],
                "Resource": "*",
            },
            {
                "Sid": "VisualEditor2",
                "Effect": "Allow",
                "Action": "sts:GetServiceBearerToken",
                "Resource": "*",
            },
        ],
    }
    bsm.iam_client.put_user_policy(
        UserName=iam_user_name,
        PolicyName=f"{iam_user_name}-inline-policy",
        PolicyDocument=json.dumps(policy_document),
    )

    # --- create or get key
    res = bsm.iam_client.list_access_keys(UserName=iam_user_name)
    access_key_list = res.get("AccessKeyMetadata", [])
    if access_key_list:
        data = json.loads(path_access_key_json.read_text())
        access_key = data["access_key"]
        secret_key = data["secret_key"]
    else:
        response = bsm.iam_client.create_access_key(UserName=iam_user_name)
        access_key = response["AccessKey"]["AccessKeyId"]
        secret_key = response["AccessKey"]["SecretAccessKey"]
        content = json.dumps(
            {"access_key": access_key, "secret_key": secret_key}, indent=4
        )
        path_access_key_json.write_text(content)
    print(f"{access_key = }")

    # --- set github secrets
    path_github_token = get_github_token_file(
        owner_username=github_username,
        token_name=github_token_name,
    )
    github_token = path_github_token.read_text().strip()

    url = f"https://github.com/{github_username}/{repo_name}/settings/secrets/actions"
    print(f"  preview at {url}")
    gh = Github(github_token)
    repo = gh.get_repo(f"{github_username}/{repo_name}")

    repo.create_secret(
        secret_name="AWS_DEFAULT_REGION",
        unencrypted_value="us-east-1",
        secret_type="actions",
    )
    repo.create_secret(
        secret_name="AWS_ACCESS_KEY_ID",
        unencrypted_value=access_key,
        secret_type="actions",
    )
    repo.create_secret(
        secret_name="AWS_SECRET_ACCESS_KEY",
        unencrypted_value=secret_key,
        secret_type="actions",
    )


if __name__ == "__main__":
    main()
