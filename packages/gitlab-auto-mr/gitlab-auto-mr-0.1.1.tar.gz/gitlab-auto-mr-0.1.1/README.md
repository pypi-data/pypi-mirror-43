![image](https://gitlab.com/hmajid2301/gitlab-auto-merge-request/badges/master/pipeline.svg%20%20:alt:%20Pipeline%20Status)

![image](https://img.shields.io/pypi/status/gitlab-auto-mr.svg%20%20:alt:%20PyPI%20-%20Status)

![image](https://img.shields.io/pypi/pyversions/gitlab-auto-mr.svg%20%20:alt:%20PyPI%20-%20Python%20Version)

# GitLab Auto MR

This script is meant to be used in GitLab CI to automatically open Merge
Requests for feature branches, if there is none yet. This project
provides a docker image you can use for ease of use, but also a Python
library.

It is based on the script and idea of [Riccardo
Padovani](https://rpadovani.com), which he introduced with his blog post
[How to automatically create new MR on Gitlab with Gitlab
CI](https://rpadovani.com/open-mr-gitlab-ci).

## Usage

- GITLAB_PRIVATE_TOKEN Set a secret variable in your GitLab project with your private token. Name it
  GITLAB_PRIVATE_TOKEN (`CI/CD > Environment Variables`). This is necessary to raise the Merge Request on your behalf.
  More information [click here](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html).

`.gitlab-ci.yml`: An example CI using this can be found
[here](https://gitlab.com/hmajid2301/stegappasaurus/blob/master/.gitlab-ci.yml)

Add the following to your `.gitlab-ci.yml` file:

```yaml
stages:
  - open

open_merge_request:
  image: registry.gitlab.com/hmajid2301/gitlab-auto-merge-request
  before_script: [] # We do not need any setup work, let's remove the global one (if any)
  variables:
    GIT_STRATEGY: none # We do not need a clone of the GIT repository to create a Merge Request
  stage: open
  only:
    - /^feature\/*/ # We have a very strict naming convention
```

## Environment Variables

You can set extra variables like so.

```yaml
variables:
  GIT_STRATEGY: none # We do not need a clone of the GIT repository to create a Merge Request
  TARGET_BRANCH: master # Target branch for MR
```

- COMMIT PREFIX: Prefix for the MR i.e. WIP
- REMOVE_BRANCH_AFTER_MERGE: Will delete branch after merge
- SQUASH: Will squash commits after merge
- AUTO_MERGE: Will auto merge request after being reviewed and CI
  passes
- TARGET_BRANCH: The target branch for the MR
- DESCRIPTION: Description of the Mr

## Authors

- Extra features: [Allsimon](https://gitlab.com/Allsimon/gitlab-auto-merge-request)
- Forked from: [Tobias L. Maier](https://gitlab.com/tmaier/gitlab-auto-merge-request)
- Docker part: [Tobias L. Maier](http://tobiasmaier.info)
- Script and idea: [Riccardo Padovani](https://rpadovani.com)
