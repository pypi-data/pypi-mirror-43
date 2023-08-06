=====================
Sensee Kehl Tools Api
=====================

Setup a developer environment
=============================

You need a virtualenv
---------------------

  `virtualenv -p python3.6 venv`

or

  `python3.6 -m venv venv`

Activate your virtualenv

  source venv/bin/activate

.. note:: Every command from now must be runned with your virtualenv activated

Installation
------------

From within the project directory, check available make commands

    `make help`

Setup a developer environment (install python dependencies, create a new database and install the blok)

    `make setup-dev`


Install python testing dependencies and create a test database.

    `make setup-tests`

Test suite
-----------

Run unit tests

    `make test`

Run code syntactic check (flake8)

    `make lint`

Interpreter
-----------

Use the interactive python api (See `Anyblok Book`_ to dive in AnyBlok concepts)

    `anyblok_interpreter -c app.dev.cfg`

http server
-----------

The development server runs at localhost:8080

  `make run-dev`

npm development server
----------------------

Launch the npm development server with hot reload

   `make run-dev-npm`

Build assets
------------

We need to build js and scss assets for production if modified before any push

   `make build-assets`

Create a new user
-----------------

To access the backend interface or the json rest api endpoints you need to authenticate with user credentials.

Use the interactive python api

   `anyblok_interpreter -c app.dev.cfg`

Insert a new user

   `registry.User.insert(login='johndoe',first_name='John',last_name='Doe',email='j.doe@anyblok.com')`

Insert a password for this new user

   `registry.User.CredentialStore.insert(login='johndoe',password='azerty')`

Add don't forget to commit:

   `registry.commit()`

You can now authenticate to backend through http://localhost:8080
To access the api

   `http :8080/api/v1/users -a johndoe:azerty`

Build documentation
-------------------

The html documentation files will be generated

  `make documentation`

Tmuxp user
----------

You can launch a developer screen which cleanup project, run developement
services, tests and lint with `tmuxp`_ . 
(note: you must have a virtualenv named venv in current directory in order to
make it run)

  `tmuxp load .tmuxp..dev.yaml`

Features
========

* TODO

Project
=======

Author
------

Franck Bret 
f.bret@sensee.com

Credits
-------

This `Anyblok`_ package was created with `audreyr/cookiecutter`_ and the `AnyBlok/cookiecutter-anyblok-project`_ project template.

.. _`Anyblok`: https://github.com/AnyBlok/AnyBlok
.. _`Anyblok Book`: https://anyblok.gitbooks.io/anyblok-book/content/
.. _`AnyBlok/cookiecutter-anyblok-project`: https://github.com/Anyblok/cookiecutter-anyblok-project
.. _`audreyr/cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`tmuxp`: https://pypi.org/project/tmuxp/
