analyze_objects
===============

*analyze_objects* contains command line tools that analyze compile object files (.o, .obj). It is a wrapper around the
platform specific tools ``nm`` (linux) or ``dumpbin`` (windows).

Currently, it consists of the single shell command ``find_symbols``.

Installing
----------

Install from pip::

    python -m pip install analyze_objects

Usage
-----

If binaries of installed python packages are added to the PATH, you can call ``find_symbols`` directly from the shell::

    find_symbols

Otherwise, it can be invoked using python::

    python -m analyze_objects.find_symbols

Examples
--------

Use the following command to search the object files ``foo.o`` and ``bar.o`` for undefined symbols that match the
regular expression ``"foo"``::

    find_symbols --undef_regex foo foo.o bar.o

Using this command requires that ``nm`` (linux) or ``dumpbin`` (windows) are available in the PATH. If that is not the
case, you can use the ``--nm_exe`` or ``--dumpbin_exe`` arguments to pass their location to ``find_symbols``. For
convenience, you may pass ``--store_config`` in addition to ``--nm_exe`` or ``--dumpbin_exe``, so that this path will be
used in all subsequent calls to ``find_symbols``. The stored configuration can be cleared using ``--clear_config``.

Use ``--def_regex`` instead of ``--undef_regex`` to search for defined symbols. It is
possible to combine both arguments and search for both defined and undefined symbols.

The ``find_symbols`` command accepts an arbitrary number of object files. It is possible to use placeholders ``**`` and
``*`` in the object file paths.
