### Code Structure

```
recite
|-> app                                 (recite webapp)
|   |-> static                          (static web resources)
|   |   |-> css                         (CSS folder)
|   |   |   |-> lib                     (external CSS libraries)
|   |   |   |   '-- bootstrap.min.css
|   |   |   '-- style.css               (custom styles for recite)
|   |   |-> img                         (images folder)
|   |   |   '-- favicon.ico             (favicon for recite)
|   |   |-> js                          (JS folder)
|   |   |   |-> lib                     (external JS libraries)
|   |   |   |   |-- bootstrap.min.js
|   |   |   |   '-- jquery.min.js
|   |   |   '-- recite.js               (handles user input via browsers)
|   |-> templates                       (HTML pages)
|   |   |-- about.html
|   |   |-- index.html
|   |   '-- layout.html
|   |-- __init__.py                     (app init file)
|   |-- models.py                       (schema definitions for the app)
|   |-- utils.py                        (app utilities)
|   '-- views.py                        (pages rendering for app)
|-> instance                            (environment config folder, optional)
|   '-- config.py                       (environment config file, optional)
|-- config.py                           (main config file)
|-- export.py                           (DB export tool, *executable)
|-- freshdb.py                          (DB refresh tool, *executable)
|-- README.md                           (main readme file)
|-- code_structure.md                   (the file you are looking at)
|-- create_apa_cites.md                 (doc. for how to create APA cites)
|-- RELEASES.md                         (app release logs)
|-- requirements.txt                    (required python libraries)
|-- run.py                              (module for starting app, *executable)
|-- setup.sh                            (setup, install & start app, *executable)
'-- wsgi.ini                            (WSGI server setting)
```
