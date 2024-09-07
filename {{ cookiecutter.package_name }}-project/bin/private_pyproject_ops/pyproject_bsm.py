# -*- coding: utf-8 -*-

import typing as T
import os
import dataclasses
from functools import cached_property

from boto_session_manager import BotoSesManager

from .runtime import IS_CI

if T.TYPE_CHECKING:  # pragma: no cover
    from .pyproject import PyProjectOps


@dataclasses.dataclass
class PyProjectBsm:
    """
    Namespace class for dependencies management related automation.
    """

    aws_profile: str = dataclasses.field()

    @cached_property
    def bsm(self: "PyProjectOps") -> BotoSesManager:
        if IS_CI:
            # in CI, we get the region from the environment variable
            return BotoSesManager(region_name=os.environ["AWS_DEFAULT_REGION"])
        else:
            return BotoSesManager(profile_name=self.aws_profile)
