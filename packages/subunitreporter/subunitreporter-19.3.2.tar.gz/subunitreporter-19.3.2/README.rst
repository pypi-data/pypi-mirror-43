subunitreporter
===============

.. image:: http://img.shields.io/pypi/v/subunitreporter.svg
   :target: https://pypi.python.org/pypi/subunitreporter
   :alt: PyPI Package

What is this?
-------------

subunitreporter is a plugin for Twisted Trial which adds two new reporters.
The ``subunitv2`` reporter emits subunit v2 result streams with timing information.
The ``subunitv2-b64`` reporter emits the same information, base64-encoded.
The ``subunitv2-file`` reporter emits the same information,
written directly to a file instead of the normal trial output stream.
The ``subunitv2-file`` reporter can also emit progress information to the normal reporting stream
(usually stdout)
to avoid falling prey to hang-detection based on amount of time with no output.

Usage Sample
------------

Use this with your trial command-lines.
For example::

  $ trial --reporter=subunitv2 ... | subunit-stats
  $ trial --reporter=subunitv2-b64 ... | base64 -d | subunit-stats
  $ SUBUNITREPORTER_OUTPUT_PATH=results.subunit2 trial --reporter=subunitv2-file ...
  $ SUBUNITREPORTER_OUTPUT_PATH=results.subunit2 trial --rterrors --reporter=subunitv2-file ...

Installing
----------

To install the latest version of subunitreporter using pip::

  $ pip install subunitreporter

For additional development dependencies, install the ``dev`` extra::

  $ pip install subunitreporter[dev]

Testing
-------

subunitreporter uses pyunit-style tests.
After installing the development dependencies, you can run the test suite with trial::

  $ pip install subunitreporter[dev]
  $ trial subunitreporter

License
-------

subunitreporter is open source software released under the MIT License.
See the LICENSE file for more details.
