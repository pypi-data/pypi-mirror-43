# PySqliteQueue

[![Build Status](https://travis-ci.com/mrk-andreev/PySqliteQueue.svg?branch=master)](https://travis-ci.com/mrk-andreev/PySqliteQueue) [![Maintainability](https://api.codeclimate.com/v1/badges/6193af027c24e08e7422/maintainability)](https://codeclimate.com/github/mrk-andreev/PySqliteQueue/maintainability)


```python
from pysqlitequeue import SqliteQueue

q = SqliteQueue(database=':memory:')

q.put({'key': 'value'})

q.peek() # Retrieves, but does not remove, the head of this queue, or returns null if this queue is empty.
q.poll() # Retrieves and removes the head of this queue, or returns null if this queue is empty.

q.size()
q.empty()
q.full()
```