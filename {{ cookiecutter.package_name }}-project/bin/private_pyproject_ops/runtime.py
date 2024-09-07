# -*- coding: utf-8 -*-

"""
**"Runtime" Definition**

Runtime is where you execute your code. For example, if this code is running
in a CI build environment, then the runtime is "ci". If this code is running
on your local laptop, then the runtime is "local". If this code is running on
AWS Lambda, then the runtime is "lbd"

This module automatically detect what is the current runtime.

.. note::

    This module is "ZERO-DEPENDENCY".
"""

import os


class RuntimeEnum:
    """
    This code will only be run either from local laptop or CI environment.
    It won't be run from Lambda Function. For EC2, it considers EC2 the
    same as your local laptop.
    """

    local = "local"
    ci = "ci"


# In this project, we use Codebuild as the CI build environment
# See https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-env-vars.html
if "CI" in os.environ:
    CURRENT_RUNTIME = RuntimeEnum.ci
    IS_CI = True
    IS_LOCAL = False
else:
    CURRENT_RUNTIME = RuntimeEnum.local
    IS_CI = False
    IS_LOCAL = True
