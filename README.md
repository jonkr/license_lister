# licence_lister

A simple tool wrapping [yolk3k](https://github.com/myint/yolk) allowing you to easily generate a list of all your dependencies and their corresponding licences based on the contents of your `requirements.txt`-files(s).

### Installation
```
$ pip install license_lister
```

### How to use
Basic invocation:

```
$ license_lister -p /path/to/some/repository/
```

Multiple repositories at once:

```
$ license_lister -p /path/to/repository-1 -p /path/to/repository-2
```

### Example output
```
$ license_lister -p /path/to/basic/webapp/
alembic      MIT
boto         MIT
coverage     Apache 2.0
Flask        BSD
gevent       MIT
Jinja2       BSD
psycopg2     LGPL with exceptions or ZPL
```