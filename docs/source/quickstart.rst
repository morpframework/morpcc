=====================
Quick Start Tutorial
=====================


iInstalling
===========

The recommended installation method is to use pipenv, or you can also use pip::

  pip install morpcc==0.1.0a2

MorpCC includes a demo CMS for testing purposes, you can start it up through::

  wget https://raw.githubusercontent.com/morpframework/morpcc/master/morpcc/tests/democms/settings.yml 
  morpfw register-admin -s settings.yml -u admin -e admin@localhost.local
  morpfw start -s settings.yml

That will start the demo CMS at http://localhost:5432/

Creating new project
==========================

To create new project, you can initialize using cookiecutter-morpcc::

  pip install cookiecutter
  cookiecutter https://github.com/morpframework/cookiecutter-morpcc

And start your project using::

  morpfw register-admin -s settings.yml -u admin -e admin@localhost.local
  morpfw start -s settings.yml


Creating new content type
==========================

To create new content type, first, enter your project module where ``app.py`` 
resides, then::

  cookiecutter https://github.com/morpframework/cookiecutter-morpcc-type

This will generate a basic content type to work with. Load the url you provide 
for the ui mount path to see the collection. (eg: if you specified ``/content``, 
load http://localhost:5432/content/ )
