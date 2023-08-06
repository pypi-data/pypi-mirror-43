Delbot
======

A service status blog for SaaS applications

![Build](https://git.steadman.io/podiant/delbot/badges/master/build.svg)
![Coverage](https://git.steadman.io/podiant/delbot/badges/master/coverage.svg)

## Quickstart

Install Delbot:

```sh
pip install delbot
```

Run it:

```sh
python manage.py migrate
python manage.py runserver
```

## Running tests

Does the code actually work?

```sh
coverage run --source delbot manage.py test
```

## Credits

Tools used in rendering this package:

- [Cookiecutter](https://github.com/audreyr/cookiecutter)
- [`cookiecutter-djangopackage`](https://github.com/pydanny/cookiecutter-djangopackage)
