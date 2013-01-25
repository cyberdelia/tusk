====
Tusk
====

Installing
==========

To install : ::

    pip install tusk


Usage
=====

Tusk tries to be as simple as possible ::

    l = Lock("postgres://localhost/noclue")
    l.acquire("inspector", blocking=True)
    t.release("inspector")

