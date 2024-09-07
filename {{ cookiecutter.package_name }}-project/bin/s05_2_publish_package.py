#!/usr/bin/env python
# -*- coding: utf-8 -*-

from private_pyproject_ops.main import pyops

pyops.twine_authorization()
pyops.publish_to_codeartifact()
