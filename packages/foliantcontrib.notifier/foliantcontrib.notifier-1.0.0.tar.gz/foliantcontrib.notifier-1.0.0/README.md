# GitLab notifier config tool

CLI extension for Foliant to set up [GitLab notifier](https://gitlab.com/ddddsa/gitlab_notifier) config for the project.

## Installation

```bash
$ pip install foliantcontrib.notifier
```

## Usage

> Note that to use this command you will have to specify valid [config](#config) first!

Apply notifications for this repo:

```bash
$ foliant notifier setup
```

Disable notifications in this repo:

```bash
$ foliant notifier disable
```

## Config

Before running notifier command you will have to supply valid config. Set it up under the `notifier` section in your `foliant.yml`.

In basic form `notifier` contents should be filled as explained in [GitLab notifier Config section](https://gitlab.com/ddddsa/gitlab_notifier#config), for example:

```yaml
notifier:
    mail_config:
        host: mail.example.com
        port: 587
        user: notifier@example.com
        password: currently_stored_as_plain_text
    projects:
        test-project:
            - match:
                - test1.txt
                - test/file1.txt
              mailing_list:
                - john@gmail.com
                - sam@gmail.com
            - mailing_list:
                - sam@gmail.com
              match:
                - test1.txt
                - test/*
              ignore:
                - file3.txt
```

`mail_config` — Credentials of the mail server account which will send the notifications.

`projects` — section, describing GitLab-projects which are being tracked.

`test-project` — name of the project. That one which you see in your browser address bar: gitlab.com/username/**test-project**. In our case this should be the name of our foliant-project in GitLab.

Next goes a list with tracking settings. Each group can have following sections:

`mailing_list` — list of email-addresses, which will receive notifications.

`match` — list of [glob](https://en.wikipedia.org/wiki/Glob_(programming))-like patterns. If files in the repository, which match these patterns, are changed, script will send notifications to the mailing_list, set up in this group.

`ignore` — list of glob-like patterns of files to ignore.

### Additional options

Preprocessor also has some additional options which allow to tune its behavior:

```yaml
notifier:
    repo_url: 'https://gitlab.com/ddddsa/gitlab_notifier.git'
    config: 'notifier_config.yml'
    stage: 'notify'
    job: 'notifier'
    image: 'python:latest'
    branches:
        - 'develop'
    python: 3
```

`repo_url`
:   URL of the GitLab notifier script repository to be used.

`config`
:   Name of the generated config file for the script.

`stage`
:   Name of the stage to used in the job in `.gitlab-ci.yml`.

`job`
:   Job name for the notifier in `.gitlab-ci.yml`.

`image`
:   Name of the Docker image to be used to run the script. Default is `python:latest`. Set to empty string `''` to use `.gitlab-ci.yml` global image.

`branches`
:   List of branch names for which the notifications are enabled.

`python`
:   Python version which is used in the Docker image which will run the script.
