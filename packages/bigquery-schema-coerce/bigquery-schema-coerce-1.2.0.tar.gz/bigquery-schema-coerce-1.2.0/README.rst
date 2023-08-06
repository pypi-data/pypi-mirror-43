bigquery-schema-coerce
==============

.. image:: https://badge.fury.io/py/bigquery-schema-coerce.png
    :target: https://badge.fury.io/py/bigquery-schema-coerce

.. image:: https://travis-ci.org/narfman0/bigquery-schema-coerce.png?branch=master
    :target: https://travis-ci.org/narfman0/bigquery-schema-coerce

Force python dictionary to type convert into the given bigquery schema

Installation
------------

Install via pip::

    pip install bigquery-schema-coerce

Usage
-----

Import and parse schema with::

    import bigquery_schema_coerce as bqcoerce
    schema = list(bqcoerce.parse_schema(path='schema.json'))

We may then type convert python objects (dictionaries) with::

    result = bqcoerce.coerce(object, schema)

Check our unit tests for a small example. We can limit to
type conversion or projecting using `bqcoerce.convert` or `bqcoerce.project`.

Note: parse_schema returns a generator, which can only be iterated once. Since with bigquery
a user would likely be iterating over many objects, it is wise to by default create a list,
but the option remains if performance is needed to only use the generator.

Development
-----------

Ensure you have pipenv installed to manage dependencies.

Run suite to ensure everything works::

    make test

Release
-------

To publish your plugin to pypi, sdist and wheels are (registered,) created and uploaded with::

    make release

TODO
----

* If field is nullable and empty (e.g. ""), remove
* Ingest schema from bigquery api
* Deal with more complex records, perhaps GEOGRAPHY or ingesting a STRING and
  ensuring common formats are OGC Simple Features Specification

License
-------

Copyright (c) 2018 Jon Robison

See LICENSE for details
