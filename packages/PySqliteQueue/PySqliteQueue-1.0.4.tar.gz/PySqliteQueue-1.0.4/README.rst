PySqliteQueue
============
.. image:: https://travis-ci.org/mrk-andreev/PySqliteQueue.svg?branch=master
    :target: https://travis-ci.org/mrk-andreev/PySqliteQueue

.. image:: https://api.codeclimate.com/v1/badges/6193af027c24e08e7422/maintainability
   :target: https://codeclimate.com/github/mrk-andreev/PySqliteQueue/maintainability
   :alt: Maintainability


.. image:: https://badge.fury.io/py/PySqliteQueue.svg
    :target: https://badge.fury.io/py/PySqliteQueue

.. image:: https://img.shields.io/pypi/l/PySqliteQueue.svg

User installation
~~~~~~~~~~~~

  pip install -U PySqliteQueue

Example
~~~~~~~~~~~~


  from pysqlitequeue import SqliteQueue

  q = SqliteQueue(database=':memory:')

  q.put({'key': 'value'})

  q.peek() # Retrieves, but does not remove, the head of this queue, or returns null if this queue is empty.
  
  q.poll() # Retrieves and removes the head of this queue, or returns null if this queue is empty.

  q.size()
  q.empty()
