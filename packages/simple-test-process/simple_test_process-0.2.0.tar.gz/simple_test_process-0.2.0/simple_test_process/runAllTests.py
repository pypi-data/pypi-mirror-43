# ------- #
# Imports #
# ------- #

from traceback import format_exc
from .fns import forEach


# ---- #
# Main #
# ---- #


def runAllTests(stateOrSuite):
    forEach(runTest)(stateOrSuite.tests)
    forEach(runAllTests)(stateOrSuite.suites)


# ------- #
# Helpers #
# ------- #


def runTest(aTest):
    try:
        aTest.fn()
        aTest.succeeded = True
    except Exception as e:
        aTest.succeeded = False
        aTest.rootState.succeeded = False
        propagateFailure(aTest.parentSuite)
        aTest.formattedException = format_exc()
        aTest.error = e


def propagateFailure(aSuite):
    if aSuite is None:
        return

    if aSuite.succeeded:
        aSuite.succeeded = False
        propagateFailure(aSuite.parentSuite)
