# -*- coding: utf-8 -*-

"""
The upstream concrete repo is ``aws_python-project``. This script can convert
the concrete repo into a project template.
"""

import shutil
from pathlib import Path
from cookiecutter_maker.maker import Maker

dir_here: Path = Path(__file__).absolute().parent
dir_tmp = dir_here.joinpath("tmp")
if dir_tmp.exists():
    shutil.rmtree(dir_tmp)
dir_tmp.mkdir(parents=True, exist_ok=True)

maker = Maker.new(
    # the input concrete project directory
    input_dir=Path.home().joinpath("Documents", "GitHub", "aws_code_artifact_python_example-project"),
    # the output template project directory
    output_dir=dir_tmp,
    # define the pair of ``concrete string`` and ``parameter name``
    mapper=[
        # fmt: off
        # real value, variable name, default value
        ("aws_code_artifact_python_example", "package_name", "your_package_name"),
        ("MacHu-GWU", "github_username", "your_github_username"),
        ("Sanhe Hu", "author_name", "Author Name"),
        ("husanhe@gmail.com", "author_email", "author@email.com"),
        ("0.1.1", "semantic_version", "0.1.1"),
        ("bmt_app_devops_us_east_1", "aws_profile", "your_aws_profile"),
        ("bmt-python", "aws_codeartifact_repository", "your_aws_codeartifact_repository"),
        ("bmt", "aws_codeartifact_domain", "your_aws_codeartifact_domain"),
        ("862612136886", "aws_account_id", "111122223333"),
        ("sanhe-dev", "github_token_name", "your_github_token_name"),
        # fmt: on
    ],
    # define what to include in the input directory
    # it is the relative path from the input directory
    # the rule is 'explicit exclude' > 'explicit include' > 'default include'
    include=[],
    # define what to exclude in the input directory
    # it is the relative path from the input directory
    exclude=[
        # dir
        ".venv",
        ".pytest_cache",
        ".git",
        ".idea",
        "build",
        "dist",
        "htmlcov",
        "__pycache__",
        "tmp",
        "docs/source/aws_code_artifact_python_example",
        # file
        ".coverage",
    ],
    # overwrite the output location if already exists
    overwrite=True,
    # mapper could have one key is substring of another key
    # if this is True, it will ignore the error
    ignore_mapper_error=False,
    # when mapper could have one key is substring of another key
    # it will prompt you to confirm to continue
    skip_mapper_prompt=False,
    # do you want to print debug information?
    debug=True,
)
maker.templaterize()
