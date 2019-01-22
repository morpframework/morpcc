=============
Introduction
=============

Morp Control Center (morpcc) is a meta information management system (IMS)
built on top of `Morp Framework (morpfw) <http://morpframework.rtfd.org>`_ &
`Morepath <http://morepath.rtfd.org>`_. 
It is designed to provide common components needed for the the development
of IMSes while allowing flexibility for developers to customize and override
the components. Key components provided includes:

* Responsive default UI based on `Gentelella 
  <https://github.com/puikinsh/gentelella>`_ project

* Pluggable auth system

  * User, group & API key management system (SQLAlchemy based)

  * REMOTE_USER based authentication

* Content type framework and CRUD UI

* Pluggable CRUD storage backend

  * SQLAlchemy (default)
 
  * ElasticSearch

  * Dictionary based, in-memory

* Listing / search interface with JQuery DataTables server-side API

* Pluggable blob storage backend

  * Filesystem store (default)

* REST API through morpfw content type API engine with JWT based token

* Statemachine engine using PyTransitions through morpfw

* Overrideable components and templates through
  `morepath <http://morepath.rtfd.org>`_ & `dectate <http://dectate.rtfd.org>`_
  app inheritance

Design
=======

morpcc and morpfw design is highly influenced by `Plone <http://plone.org>`_
project. Unlike frameworks such as Django, Pyramid, and Flasks routing which
routes to views, morpcc/morpfw routing routes to an object/model publisher.
Views are attached to model and goes around with the model. 
This design gives the framework certain benefits:

* Views and view templates are highly reusable because as long as the model
  implements the attributes and methods the view queries, the view can be
  attached to the model.

* Views can be inherited by sub-models. You can create mixin interface classes
  and attach the views to it. Any models which inherits from the mixin will get
  the view.

* Views follows model and its sub-models. Whatever path the model is mounted,
  the views for the model will follow.

* -More benefits here-
