=====================
Quick Start Tutorial
=====================

Installation
==============

Basic installation
-------------------

The recommended installation method is to use 
`pipenv <http://pipenv.rtfd.org>`_, or you can also use pip or virtualenv.

If you dont have pipenv installed yet, do:

.. code-block:: bash

   sudo pip install pipenv>=2018.11.26

lets install morpcc into a pipenv:

.. code-block:: bash

   mkdir morpcc
   cd morpcc
   pipenv install morpcc==0.1.0a2

MorpCC includes a demo CMS for testing purposes, you can start it up through:

.. code-block:: bash
  
   wget https://raw.githubusercontent.com/morpframework/morpcc/master/morpcc/tests/democms/settings.yml 
   pipenv run morpfw register-admin -s settings.yml -u admin -e admin@localhost.local
   pipenv run morpfw start -s settings.yml

That will start the demo CMS at http://localhost:5432/

Installation as a new project
------------------------------

To create new project, you can initialize using cookiecutter-morpcc:

.. code-block:: bash

   sudo pip install cookiecutter
   cookiecutter https://github.com/morpframework/cookiecutter-morpcc

And start your project using:

.. code-block:: bash

   cd $PROJECTNAME/ # replace with your project directory name
   pipenv install .
   pipenv run morpfw register-admin -s settings.yml -u admin -e admin@localhost.local
   pipenv run morpfw start -s settings.yml


Creating new content type
==========================

To create new content type, first, enter your project module where ``app.py`` 
resides, then:

.. code-block:: bash

   pipenv run cookiecutter https://github.com/morpframework/cookiecutter-morpcc-type

This will generate a basic content type to work with. Load the url you provide 
for the ui mount path to see the collection. (eg: if you specified ``/content``, 
load http://localhost:5432/content/ )


Understanding core framework functionalities
=============================================

MorpCC is built on top of Morepath, so we suggest you head to `Morepath 
Documentation <http://morepath.rtfd.org>`_ for guide on how to register your
own views, etc.

The templating language used is TAL, and we extensively use METAL for template
inheritance. Head to `Chameleon TAL/METAL Language Reference <https://chameleon.readthedocs.io/en/latest/reference.html>`_
and `Zope Page Template Reference <https://zope.readthedocs.io/en/latest/zope2book/AppendixC.html>`_
to understand more about TAL and METAL.

