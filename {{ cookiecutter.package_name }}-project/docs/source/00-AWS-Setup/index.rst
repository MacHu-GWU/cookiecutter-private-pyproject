AWS Setup
==============================================================================
这个项目使用了 AWS Code Artifact 来发布 Python Package, 并使用了 GitHub Action 来进行 CI. 所以为了能让 GitHub Action 的运行环境中能跟 AWS 交互, 我们需要在 GitHub 项目中设置 AWS 的 Secrets. 这里我们没有使用 Fancy 的 OIDC 来进行认证, 而是使用了最简单的 AWS IAM USER 的 Access Key 和 Secret Key + Environment Variable 来进行授权.

.. dropdown:: aws_setup.py

    .. literalinclude:: ./aws_setup.py
       :language: python
       :emphasize-lines: 1-1
       :linenos:
