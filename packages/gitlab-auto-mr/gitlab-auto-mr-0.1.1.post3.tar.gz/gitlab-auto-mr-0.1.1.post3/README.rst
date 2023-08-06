.. image:: https://gitlab.com/hmajid2301/gitlab-auto-merge-request/badges/master/pipeline.svg

.. image:: https://img.shields.io/pypi/status/gitlab-auto-mr.svg

.. image:: https://img.shields.io/pypi/pyversions/gitlab-auto-mr.svg

GitLab Auto MR
==============

This is a simple Python script that allows you create MR in GitLab automatically. It is intended to be used in CI/CD
as a Docker image. However you can use it as a separate Python library if you would like.
An example CI using this can be found `here <https://gitlab.com/hmajid2301/stegappasaurus/blob/master/.gitlab-ci.yml>`_.

It is based on the script and idea of `Riccardo Padovani <https://rpadovani.com>`_, which he introduced with his blog post
`How to automatically create new MR on Gitlab with Gitlab CI <https://rpadovani.com/open-mr-gitlab-ci>`_.
Thanks for providing this.

This package was intended to be used by GitLab CI hence using environments provided by the GitLab CI. You can however
use it as a CLI tool if you would like.

Usage
-----

First you need to create a personal access token,
`more information here <https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html>`_.
With the scope ``api``, so it can create the MR using your API.

``pip install gitlab-auto-mr``

.. code-block::

    Usage: gitlab_auto_mr [OPTIONS]

    Options:
      --private-token TEXT      Private GITLAB token, used to authenticate when
                                calling the MR API.  [required]
      --source-branch TEXT      The source branch to merge into.  [required]
      --project-id INTEGER      The project ID on GitLab to create the MR for.
                                [required]
      --project-url TEXT        The project URL on GitLab to create the MR for.
                                [required]
      --user-id INTEGER         The GitLab user ID to assign the created MR to.
                                [required]
      --target-branch TEXT      The target branch to merge onto.
      --commit-prefix TEXT      Prefix for the MR title i.e. WIP.
      --remove-branch BOOLEAN   Set to True if you want the source branch to be
                                removed after MR.
      --squash-commits BOOLEAN  Set to True if you want commits to be squashed.
      --description TEXT        Description in the MR.
      --help                    Show this message and exit.


.. code-block::

    gitlab_auto_mr --private-token $(private_token) --source-branch feature/test --project-id 5
                   --project-url https://gitlab.com/hmajid2301/stegappasaurus --user-id 5
