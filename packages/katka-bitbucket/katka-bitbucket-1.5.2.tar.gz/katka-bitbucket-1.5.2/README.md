# Katka Bitbucket

Django app which will be responsible for all interactions with bitbucket on Katka.

## Clone
You can clone this repository on: https://github.com/kpn/katka-bitbucket

## Setup
Setup your environment:

```shell
$ make venv
```

## Stack

Katka Bitbucket is build on top of the Python framework Django and the Django Rest
Framework to build APIs. Under the hood it runs Python 3.7.

### Dependencies
* [djangorestframework](psycopg2-binary): django toolkit for building Web APIs
* [pkgsettings](pkgsettings): to manage package specific settings

[djangorestframework]: https://github.com/encode/django-rest-framework
[pkgsettings]: https://github.com/kpn-digital/py-pkgsettings

## Contributing

### Workflow
1. Fork this repository
2. Clone your fork
3. Create and test your changes
4. Create a pull-request
5. Wait for default reviewers to review and merge your PR

## Running tests
Tests are run on docker by executing
```shell
$ make test
```

Or using venv
```shell
$ make test_local
```

## Versioning

We use SemVer 2 for versioning. For the versions available, see the tags on this 
repository.

## Authors
* *KPN I&P D-Nitro* - d-nitro@kpn.com
