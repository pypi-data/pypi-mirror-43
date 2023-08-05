1.0b7 (2019-03-10)
==================

Changes
-------

* Implement Array (CSE) Formulas

Bug Fixes
---------

* Fix #45 - Unbounded Range Addresses (ie: A:B or 1:2) broken


1.0b6 (2019-03-03)
==================

Bug Fixes
---------

* Fix #42 - 'ReadOnlyWorksheet' object has no attribute 'iter_cols'
* Fix #43 - Fix error with leading/trailing whitespace


1.0b5 (2019-02-24)
==================

Changes
-------

* Implement XOR(), NOT(), TRUE(), FALSE()
* Improve error handling for AND(), OR()
* Implement POWER() function


1.0b4 (2019-02-17)
==================

Changes
-------

* Move to openpyxl 2.6+
* Remove support for Python 3.4


1.0b3 (2019-02-02)
==================

Changes
-------

* Work around openpyxl returning datetimes
* Pin to openpyxl 2.5.12 to avoid bug in 2.5.14 (fixed in PR #315)


1.0b2 (2019-01-05)
==================

Changes
-------

* Much work to better match Excel error processing
* Extend validate_calcs() to allow testing entire workbook
* Improvements to match(), including wildcard support
* Finished implementing match(), lookup(), vlookup() and hlookup()
* Implement COLUMN() and ROW()
* Implement % operator
* Implement len()
* Implement binary base number Excel functions (hex2dec, etc.)
* Fix PI()


1.0b0 (2018-12-25)
===================

Major changes
-------------

* Converted to Python 3.4+
* Removed Windows Excel COM driver (openpyxl is used for all xlsx reading)
* Add support for defined names
* Add support for structured references
* Fix support for relative formulas
* set_value() and evaluate() support ranges and lists
* Add several more library functions
* Add AddressRange and AddressCell classes to encapsulate address calcs
* Add validate_calcs() to aid debugging excellib functions
* Add `build` feature which can limit recompile to only when excel file changes
* Improved handling for #DIV0! and #VALUE!


Compatibility
-------------

* Tests run on Python 3.4, 3.5, 3.6, 3.7 (via tox)
* Python 2 no longer supported


Other Changes
-------------

* Heavily refactored ExcelCompiler
* Moved all formula evaluation, parsing, etc, code to ExcelFormula class
* Convert to using openpyxl tokenizer
* Converted prints to logging calls
* Convert to using pytest
* Add support for travis and codecov.io
* 100% unit test coverage (mostly)
* Add debuggable formula evaluation
* Cleanup generated Python code to make easier to read
* Add a text format (yaml or json) serialization format
* flake8 (pep8) checks added
* pip now handles which Python versions can be used
* Release to PyPI
* Docs updated


Bugfixes
--------

* Numerous


0.0.1 (unreleased)
===================

* Original version available from `Dirk Ggorissen's Pycel Github Page`_.
* Supports Python 2

.. _Dirk Ggorissen's Pycel Github Page: https://github.com/dgorissen/pycel/tree/33c1370d499c629476c5506c7da308713b5842dc
