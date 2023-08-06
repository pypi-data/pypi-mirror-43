# Copyright Least Authority TFA GmbH
# See LICENSE for details.

from __future__ import (
    division,
    absolute_import,
    print_function,
    unicode_literals,
)

from os import environ, devnull
from sys import stdout
from base64 import b64encode

import attr

from zope.interface import implementer

from testtools import ExtendedToStreamDecorator
from subunit.v2 import StreamResultToBytes
from subunit.test_results import  AutoTimingTestResultDecorator

from twisted.trial.itrial import IReporter
from twisted.trial.util import excInfoOrFailureToExcInfo

def _make_subunit(reporter):
    return AutoTimingTestResultDecorator(
        ExtendedToStreamDecorator(
            StreamResultToBytes(
                reporter.stream,
            ),
        ),
    )

def _default_progress_stream():
    return open(devnull, "wb")

def _progress_stream(v):
    if v is None:
        return _default_progress_stream()
    return v

@attr.s
@implementer(IReporter)
class _SubunitReporter(object):
    """
    Reports test output using the subunit v2 protocol.

    :ivar stream: A binary-mode file-like object to which the subunit v2
        result stream will be written.

    :ivar progress_stream: A text-mode file-like object to which periodic
        progress updates will be written.
    """
    _SUCCESS_MARK = u"\N{CHECK MARK}".encode("utf-8")
    _FAIL_MARK = u"\N{MULTIPLICATION X}".encode("utf-8")
    _ERROR_MARK = u"\N{EXCLAMATION MARK}".encode("utf-8")
    _SKIP_MARK = u"\N{PICK}".encode("utf-8")
    _XFAIL_MARK = u"\N{PICK}".encode("utf-8")
    _XSUCCESS_MARK = u"\N{PICK}".encode("utf-8")

    stream = attr.ib(default=stdout)
    progress_stream = attr.ib(
        default=_default_progress_stream(),
        converter=_progress_stream,
    )

    _subunit = attr.ib(
        default=attr.Factory(
            _make_subunit,
            takes_self=True,
        ),
        repr=False,
        cmp=False,
        hash=None,
        init=False,
    )

    def done(self):
        """
        Record that the entire test suite run is finished.

        No-op because the end of a subunit protocol data stream is what
        signals completion.
        """

    def shouldStop(self):
        """
        Should the test runner should stop running tests now?
        """
        return self._subunit.shouldStop
    shouldStop = property(shouldStop)

    def stop(self):
        """
        Signal that the test runner should stop running tests.
        """
        return self._subunit.stop()

    def wasSuccessful(self):
        """
        Meaningless introspection on number of errors and failures.

        :return: ``True`` because the test runner doesn't need to know.
        """
        return True

    def startTest(self, test):
        """
        Record that ``test`` has started.
        """
        return self._subunit.startTest(test)

    def stopTest(self, test):
        """
        Record that ``test`` has completed.
        """
        return self._subunit.stopTest(test)

    def addSuccess(self, test):
        """
        Record that ``test`` was successful.
        """
        self.progress_stream.write(self._SUCCESS_MARK)
        return self._subunit.addSuccess(test)

    def addSkip(self, test, reason):
        """
        Record that ``test`` was skipped for ``reason``.

        :param TestCase test: The test being skipped.

        :param reason: The reason for it being skipped. The result of ``str``
            on this object will be included in the subunit output stream.
        """
        self.progress_stream.write(self._SKIP_MARK)
        self._subunit.addSkip(test, reason)

    def addError(self, test, err):
        """
        Record that ``test`` failed with an unexpected error ``err``.
        """
        self.progress_stream.write(self._ERROR_MARK)
        return self._subunit.addError(
            test,
            excInfoOrFailureToExcInfo(err),
        )

    def addFailure(self, test, err):
        """
        Record that ``test`` failed an assertion with the error ``err``.
        """
        self.progress_stream.write(self._FAIL_MARK)
        return self._subunit.addFailure(
            test,
            excInfoOrFailureToExcInfo(err),
        )

    def addExpectedFailure(self, test, failure, todo):
        """
        Record an expected failure from a test.
        """
        self.progress_stream.write(self._XFAIL_MARK)
        self._subunit.addExpectedFailure(
            test,
            excInfoOrFailureToExcInfo(failure),
        )

    def addUnexpectedSuccess(self, test, todo=None):
        """
        Record an unexpected success.

        Since subunit has no way of expressing this concept, we record a
        success on the subunit stream.
        """
        self.progress_stream.write(self._XSUCCESS_MARK)
        self.addSuccess(test)


def reporter(stream, tbformat=None, realtime=None, publisher=None):
    """
    Create a trial reporter which emits a subunit v2 stream of test result
    information to the given stream.

    :param stream: A ``write``-able object to which the result stream will be
        written.
    """
    return _SubunitReporter(stream=stream)


def reporter_b64(stream, tbformat=None, realtime=None, publisher=None):
    """
    Create a trial reporter which emits a base64 encoded stream of a subunit
    v2 stream of test result information to the given stream.

    This is useful when the output must be transported by a non-8-bit-clean
    protocol or transport (I'm looking at you, JSON).

    :param stream: A ``write``-able object to which the result stream will be
        written.
    """
    return _SubunitReporter(stream=_Base64Bytes(stream))


def reporter_file(stream, tbformat=None, realtime=None, publisher=None):
    """
    Create a trial reporter which emits a subunit v2 stream of test result
    information to a file identified by the ``SUBUNITREPORTER_OUTPUT_PATH``
    environment variable.

    This is useful when mixing the binary subunitv2 output into trial's output
    would be inconvenient (for example, when trial is run by tox and there is
    a desire to actually use the test result information).

    :param stream: **ignored** in favor of the file identified in the
        environment.

    :param bool realtime: If ``True`` then progress will be reported to
        ``stream`` as the test run progresses.

    :note: The value of ``realtime`` is supplied by trial based on whether
        ``--rterrors`` is given on the command line.  We're abusing the flag
        to mean something somewhat different than the intent, here, but it's
        an easy way to a boolean argument in as configuration.
    """
    if realtime:
        progress_stream = stream
    else:
        progress_stream = None
    stream = open(environ["SUBUNITREPORTER_OUTPUT_PATH"], "wb")
    return _SubunitReporter(stream=stream, progress_stream=progress_stream)


@attr.s
class _Base64Bytes(object):
    stream = attr.ib()

    def write(self, data):
        self.stream.write(b64encode(data).decode("ascii"))
        return len(data)

    def read(self, count=None):
        return b""

    def flush(self):
        return self.stream.flush()
