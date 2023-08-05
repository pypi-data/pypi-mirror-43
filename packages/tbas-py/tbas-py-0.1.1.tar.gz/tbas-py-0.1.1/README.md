# tbas_python
T🅱AS

[![Build Status](https://travis-ci.org/ehennenfent/tbas_python.svg?branch=master)](https://travis-ci.org/ehennenfent/tbas_python)

A set of tools for working with [TBAS](https://hackthebadge.com/2018-cyphercon-3-0-badge-special-message-from-the-tymkrs/)

`pip install tbas-py` to install. Requires Python 3.6+

`echo "+>++>+++D" | tbas` to run the headless interpreter

Includes a TK-based graphical debugger w/ breakpoints:

[![Screenshot](https://raw.githubusercontent.com/ehennenfent/tbas_python/master/ui.png)](https://raw.githubusercontent.com/ehennenfent/tbas_python/master/ui.png)

`echo "+>++>+++D" | tbas-gui` to run the UI

* tbas/badge_io.py - Implementations of various IO modes
* tbas/buffer.py - Implements the FIFO/FILO buffer
* tbas/corpus.py - Functions that generate TBAS programs to do useful things
* tbas/datatypes.py - Contains macros used for type hinting
* tbas/interpreter.py - User interface and driver
* tbas/machine.py - Contains class that tracks machine state
* tests/tests.py - unit tests
* tbas/ui.py - main UI class
* tbas/util.py - Helper functions
