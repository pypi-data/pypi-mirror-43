

<p align="center">
  <img align="center" src="frontend/src/assets/logo-brand.png" alt="Logo" width="180"/>
</p>

DbNet is a Python/VueJS database client to access Oracle, Spark (Hive), Postgres, etc. It is still a work in progess, but should work fine for daily use. MS SQL Server is supported, although with some bugs here and there due to JDBC/JTDS bridge.

**Only Chrome and Firefox are supported at the moment.**

# Install
```bash
pip install dbnet
```

Command `dbnet` should now be available in the PATH.

# Running

`dbnet --help`

```bash
usage: dbnet [-h] [--serve] [--init_db] [--reset_db] [--force] [--port PORT]

DbNet Application

optional arguments:
  -h, --help   show this help message and exit
  --serve      Start the DbNet server
  --init_db    Initiatlize the backend SQLite database
  --reset_db   Reset the backend SQLite database
  --force      Kill any running instance.
  --port PORT  The web application port
```

`dbnet --serve`

```bash
2019-02-27 10:08:11 -- DB Tables OK.
2019-02-27 10:08:11 -- Main Loop PID is 39685
2019-02-27 10:08:11 -- Monitor Loop PID is 39691
2019-02-27 10:08:11 -- Web Server PID is 39692
2019-02-27 10:08:11 -- URL -> http://macbook:5566/?token=CqPahSJIeg1Nl4Kj
(39692) wsgi starting up on http://0.0.0.0:5566
```

## Setting up Dababase Profile

Your database profile / credentials needs to be set up at `~/profile.yaml` or env var `PROFILE_YAML`.
Run command `xutil-create-profile` to create from template.

### Example Entry

```yaml
PG_XENIAL:
  name: PG_XENIAL
  host: xenial-server
  database: db1
  port: 5432
  user: user
  password: password
  type: postgresql
  url: "jdbc:postgresql://xenial-server:5432/db1?&ssl=false"
```


# Screenshots

![Screenshot 2](dbnet.screenshot.2.png)

![Screenshot 1](dbnet.screenshot.1.png)

<img src="dbnet.screenshot.schema.png" alt="Screenshot schema" width="300"/>

# Development

## Building

```bash
git clone https://github.com/flarco/dbnet.git
cd dbnet
bash build.sh
```

## Release

- Update version in [setup.py](./setup.py).
- Draft new release on Github: <https://github.com/flarco/dbnet/releases/new>

```
git clone https://github.com/flarco/dbnet.git
cd dbnet
m2r --overwrite README.md
python setup.py sdist && twine upload dist/*
```
