pubsub-split
==============

.. image:: https://badge.fury.io/py/pubsub-split.png
    :target: https://badge.fury.io/py/pubsub-split

.. image:: https://travis-ci.org/narfman0/pubsub-split.png?branch=master
    :target: https://travis-ci.org/narfman0/pubsub-split


GCP Pubsub requires messages to be less than a certain size. This library
splits collections of items to ensure that limit is not reached.

Note: Assumes users are commonly sending lists of items, rather than
large or complex python data types or dictionaries.

Installation
------------

Install via pip::

    pip install pubsub-split

Usage
-----

Import and parse schema with::

    import pubsub_split
    ...
    items = [dict(name='item1'), dict(name='item2')]
    pubsub_split.send(topic, items)

Check our unit tests for a small example.

Note: you may send keyword arguments in `send` to add additional metadata to
the envelope.

Development
-----------

Ensure you have pipenv installed to manage dependencies.

Run suite to ensure everything works::

    make test

Release
-------

To publish your plugin to pypi, sdist and wheels are (registered,) created and uploaded with::

    make release

License
-------

Copyright (c) 2019 Jon Robison

See LICENSE for details
