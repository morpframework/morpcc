===============
Content Type
===============

MorpCC object management revolves around the idea of content type. A content
type represents a data model and its respective fields. Content type definition
consist of a Schema, a Collection and a Model class. Collection is very similar
to the concept of database table, and model is very similar to a row. Model
have a Schema which defines the columns available in the Model.

When designing your application, it helps to think and model your application
around the concept of content type model and collections because views are
attached to them.

Schema
=======

Content type schema in MorpCC is defined through new python 3.7 `dataclass
library <https://docs.python.org/3/library/dataclasses.html>`_.

Schema in MorpCC/MorpFW is primarily used for data validation of
JSON/dictionary data that is used to create a new instance of content type.

When defining a schema, it is good that you inherit from ``morpfw.Schema``
as it defines the core metadata required for correct function of the framework.

.. code-block:: python

   import morpfw
   import typing
   from dataclasses import dataclass

   @dataclass
   class MySchema(morpfw.Schema):

       field1: typing.Optional[str] = None
       field2: str = 'hello world'

Due to the nature of `dataclass inheritance <https://docs.python.org/3/library/dataclasses.html#inheritance>`_,
your field definition must include default values, and if it does not have any,
you should define the field with ``typing.Optional`` data type.
