## Install, Run, and Configure

* [Installation](#installation)
    - [System Requirements](#system-requirements)

* [Run](#run)
    - [Development Mode](#development-mode)
    - [Production Mode](#production-mode)

* [Configure](#configure)

------

### Install

To install the application, run [setup.sh](setup.sh). `setup.sh` is a `bash` script that does the following:

* Installs all the requirements listed in [System requirements](#system-requirements).
* Configures the program to run as a service via `systemd`.
* Sets up and configures the `PostgreSQL` db. Creates database, users, etc.
* Starts `recite` and `PostgreSQL`.

The script was created to support the **Ubuntu** distro. The script has been successfully tested on **Ubuntu 16.04 LTS**.

#### System Requirements

* Ubuntu/Debian (prefer **Ubuntu 16.04 LTS** or **Debian8 Jessie**)
* python3 (3.5.x), python3-dev
* build-essential, postgresql, postgresql-contrib
* python3 libraries: Flask, Flask-SQLAlchemy, Jinja2, psycopg2-binary, uwsgi, python-Levenshtein

### Run

You can run the application in **Development** and **Production** modes.

##### Development Mode

Development mode is intended to be used for testing only. In order to run the program in development mode, execute [run.py](run.py) to start the  local-built-in web server. 

```bash
$> cd /path/to/recite
$> ./run.py
```

By default, the server is configured to listen on **TCP port 5000**.

##### Production Mode

Production mode cannot be run by directly calling [run.py](run.py). Production mode will be run and hosted via a dedicated web server. We currently use `uwsgi` as the web server for the application.

You will need to run [setup.sh](setup.sh) (mentioned above) to install the web server, host the web resources, and register the program and components to be called and run as a system service.

[run.py](run.py) is still used in this mode but it is treated as a `WSGI` module called by the `uwsgi` web server.

Start and stop the `recite` application in production mode as follows:

```bash
$> systemctl start recite.service
$> systemctl stop recite.service
$> systemctl restart recite.service
```

[wsgi.ini](wsgi.ini) keeps the runtime config settings for the `recite` application when it is called as a `WSGI` module.

Here is its pre-built content with explanations:

```
[uwsgi]
module = run          # name of the WSGI module in the program
master = true
processes = 5         # allows 5 simultaneous processes
socket = 0.0.0.0:80   # listen address and port
protocol = http
die-on-term = true
```

### Configure

[config.py](config.py) is the main config file of the program. The settings in there are pretty self-explanatory. Edit it as needed.

If you are deploying this program to many different environments, use [instance/config.py](instance/config.py) (optional). By default, this file does not exist. Create it whenever you think it is needed. 

The settings supported in this file are the same as the main [config.py](config.py) file. **REMEMBER:** if a config item is found here, it will be overridden by the main [config.py](config.py).
