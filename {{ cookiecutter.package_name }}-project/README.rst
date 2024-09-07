{{ cookiecutter.package_name }}
==============================================================================
在企业内部的 Python 项目一般分两种:

1. 以业务逻辑为主的 Application Code, 可能会被打包成 Web 服务器, 容器镜像等.
2. 第二种是作为可复用的 Python 库, 用来提供给其他项目使用.

这个 Git repo 是一个用来演示第二种项目的目录结构应该是怎样的.

由于我个人认为最方便的 CI 工具是 GitHub Action, 最方便的私有 Repository 工具是 AWS CodeArtifact, 所以这个项目假设企业用 AWS CodeArtifact 作为私有的 PyPI Repository, 用 GitHub Action 作为 CI/CD 工具.


Features
------------------------------------------------------------------------------
- 能在本地轻松配置虚拟环境, 解决依赖关系, 安装依赖, 运行测试, 构建文档.
- 能从 AWS CodeArtifact 上拉取私有 Python 依赖.
- 能在 GitHub Action 上运行 CI/CD 流程, 对多个 OS (Linux/Windows) 以及多个 Python 版本进行测试.
- 能将 Python 项目发布到 AWS CodeArtifact.
- 能将文档部署到 AWS S3.


How it Works
------------------------------------------------------------------------------


Getting Started
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
安装运行 Automation 所需的依赖::

    pip install -r requirements-automation.txt

创建虚拟环境::

    make venv-create

安装 Python 依赖::

    make install-all

运行测试::

    make test


Doing Development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在更改了依赖关系后, 需要重新生成 ``poetry.lock``::

    make poetry-lock

重新安装最新的依赖::

    make install
    # or any of the following
    make install-dev
    make install-test
    make install-doc
    make install-automation
    make install-all

运行代码覆盖率测试::

    make cov

运行代码覆盖率测试并查看报告::

    make cov && make view-cov


Building Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
生成文档 ``文档会被生成到 ``docs/build/html`` 目录下.``::

    make build-doc

查看本地文档::

    make view-doc

生成并查看文档::

    make build-doc && make view-doc

将带版本号的文档部署到 S3::

    make deploy-versioned-doc

将最新的文档部署到 S3::

    make deploy-latest-doc

查看 S3 上的最新文档::

    make view-latest-doc


Build and Publish
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
在本地构建 Python 包::

    make build

发布到 AWS CodeArtifact::

    make publish

将特定版本的 Python 包从 AWS CodeArtifact 删除 (后悔药)::

    make remove


Configure AWS Credential in GitHub Action
------------------------------------------------------------------------------
请参考 `AWS Setup <./docs/source/00-AWS-Setup/index.rst>`_ 中的说明来为你的 GitHub Action 配置 AWS 权限, 使得 GitHub Action CI 可以从 AWS CodeArtifact 上拉取私有 Python 依赖.
