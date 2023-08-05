Changelog
=========


Unreleased_
-----------



v0.0.2 - 2019-03-12
-------------------

* Added additional unit tests.
* Fixed issue #1 preventing :code:`DataclassBuilder` from being subclassed.
* Fields beginning with an underscore will no longer be checked.


v0.0.1 - 2019-03-11
-------------------

* Added :code:`DataclassBuilder` class to wrap Python dataclasses_ with a
  factory implementing the builder pattern.
* Added :code:`build` function to construct a dataclass_ from a
  :code:`DataclassBuilder`.
* Added :code:`fields` function to extract information about the available
  fields from a :code:`DataclassBuilder`.


.. _dataclasses: https://docs.python.org/3/library/dataclasses.html
.. _dataclass: https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass

.. _Unreleased: https://github.com/mrshannon/dataclass-builder/compare/v0.0.2...HEAD
.. _v0.0.2: https://github.com/mrshannon/dataclass-builder/compare/v0.0.1...v0.0.2
