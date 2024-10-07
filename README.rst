``cookiecutter-private-pyproject``
==============================================================================


Summary
------------------------------------------------------------------------------
This is an private (enterprise) Python library project template I used for years. You can easily generate a folder structure with everything you need and start development, then publish to `PyPI <https://pypi.org/>`_.

Best practices and automation features included in this template:

- Virtualenv management
- Dependencies management
- Local unit test and code coverage test
- Build and preview documentation site locally
- Use `GitHub Action <https://github.com/features/actions>`_ for CI
- Use `AWS CodeArtifact <https://aws.amazon.com/codeartifact/>`_ for Private PyPI Repository.
- Use `AWS S3 Static Website hosting the Docs <https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html>`_ for hosting private accessible document website.


Disclaimer
------------------------------------------------------------------------------
All the best practice used in this repo is based on my career experience, and my personal opinion. I have done over 50+ private (enterprise) Python library projects. It is the best practice I am using for years. It allow me to publish a new Python library to PyPI in one hour when I got an idea. Again, it is my personal best practice, **please use it at your own risk**.


Usage
------------------------------------------------------------------------------
Enter the following command, it will use the latest template.

.. code-block:: bash

    pip install cookiecutter && cookiecutter https://github.com/MacHu-GWU/cookiecutter-private-pyproject

Or, you can use a specific released version, you can find `full list of release at here <https://github.com/MacHu-GWU/cookiecutter-private-pyproject/releases>`_.

Use specific version:

.. code-block:: bash

    cookiecutter https://github.com/MacHu-GWU/cookiecutter-private-pyproject --checkout tags/${version}

For example (v2 is the latest as of 2024-10-07)

.. code-block:: bash

    cookiecutter https://github.com/MacHu-GWU/cookiecutter-private-pyproject --checkout tags/v2

Then fill in some information::

    package_name [your_package_name_with_underscore]: ...
    github_username [your-github-username]: ...
    author_name [Firstname Lastname]: ...
    author_email [firstname.lastname@email.com]: ...
    ...

Then it will generate a Git repo folder structures like this:

- ``/.github/``: GitHub action configuration
- ``/${package_name}/...`` your python project source code
- ``/tests/...``: unit test
- ``/.coveragerc``: code coverage test config
- ``/private_pyproject_ops.json``: automation tool config file

We have an example project generated from this template `aws_code_artifact_python_example-project <https://github.com/MacHu-GWU/aws_code_artifact_python_example-project>`_. Please take a look at it.

I personally use a branch to generate code skeleton for my open source projects.

.. code-block:: bash

    cookiecutter https://github.com/MacHu-GWU/cookiecutter-private-pyproject --checkout sanhe
