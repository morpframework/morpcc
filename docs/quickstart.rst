=====================
Quick Start Tutorial
=====================

Bootstrapping new project
===========================

The recommended installation method is to use
`pipenv <http://pipenv.rtfd.org>`_, or you can also use pip or virtualenv.

If you dont have pipenv installed yet, do:

.. code-block:: bash

   sudo pip install pipenv>=2018.11.26

Lets create a new project. You can initialize new project 
using cookiecutter-morpcc:

.. code-block:: bash

   sudo pip install cookiecutter
   cookiecutter https://github.com/morpframework/cookiecutter-morpcc

And start your project using:

.. code-block:: bash

   cd $PROJECTNAME/ # replace with your project directory name
   pipenv install .
   pipenv run morpfw register-admin -s settings.yml -u admin -e admin@localhost.local
   pipenv run morpfw start -s settings.yml

This will start your project at http://localhost:5000/

MorpCC includes a demo CMS for testing purposes, you can start it up through:

.. code-block:: bash

   wget https://raw.githubusercontent.com/morpframework/morpcc/master/morpcc/tests/democms/settings.yml -O democms.yml
   pipenv run morpfw register-admin -s democms.yml -u admin -e admin@localhost.local
   pipenv run morpfw start -s democms.yml


Creating new content type
==========================

MorpCC CRUD management revolves around the concept of content type. A content
type is a definition of a data model and its related components. Content type
is usually used to refer to real-world object concepts such as as Page,
Document, Image, Event, Person, etc.

To create new content type, first, enter your project module where ``app.py``
resides, then:

.. code-block:: bash

   pipenv run cookiecutter https://github.com/morpframework/cookiecutter-morpcc-type

This will generate a basic content type to work with. Load the url you provide 
for the ui mount path to see the collection. (eg: if you specified ``/content``, 
load http://localhost:5000/content/ )


Understanding core framework functionalities
=============================================

MorpCC is built on top of Morepath, so we suggest you head to `Morepath 
Documentation <http://morepath.rtfd.org>`_ for guide on how to register your
own views, etc.

The templating language used is TAL, and we extensively use METAL for template
inheritance. Head to `Chameleon TAL/METAL Language Reference <https://chameleon.readthedocs.io/en/latest/reference.html>`_
and `Zope Page Template Reference <https://zope.readthedocs.io/en/latest/zope2book/AppendixC.html>`_
to understand more about TAL and METAL.

