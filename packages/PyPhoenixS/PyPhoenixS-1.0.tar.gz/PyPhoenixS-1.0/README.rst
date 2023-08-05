=========
PyPhoenix
=========

PyPhoenix is a `SQLAlchemy <http://www.sqlalchemy.org/>`_ interfaces for `Phoenix`

Usage
=====

First install this package to register it with SQLAlchemy (see ``setup.py``).

.. code-block:: python
    from sqlalchemy import create_engine
    e = create_engine('pyphoenix://@localhost:8765')
    res = e.execute('select count(*) from public.core_lead')
    print(res.cursor.fetchall())

Requirements
============

Install using

- ``python setup.py install --prefix=~/.local/``

PyPhoenix is officially tested with

- Python >3.6
