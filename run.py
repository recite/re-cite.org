#!/usr/bin/env python3
# -*- coding: ascii -*-

"""
This run file is used for running the application server for the project. 
It can be called directly to start the server in development (or testing) mode using
port 5000. For production use, call this file as a WSGI module, listen port 80, via
a dedicated web server program like: nginx, apache2, uWSGI (uWSGI is used by default
in this project).

For more information about how to install and run recite, please refer to "README.md".
"""

from app import app as application

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)
