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

    l = Lock("inspector", "postgres://localhost/noclue")
    l.acquire(blocking=True)
    l.release()
    with l:
        process()

