# -*- coding: utf-8 -*-

import os
from boto_session_manager import BotoSesManager
from .runtime import IS_CI

if IS_CI:
    bsm = BotoSesManager(region_name=os.environ["AWS_DEFAULT_REGION"])
else:
    bsm = BotoSesManager(profile_name="{{ cookiecutter.aws_profile }}")
