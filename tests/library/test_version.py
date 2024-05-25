import re
import thread


def test_versionIsString():
    assert isinstance(thread.__version__, str), 'thread.__version__ is not a string'


def test_versionIsSemVer():
    assert re.match(
        r'^\d+\.\d+\..+$', thread.__version__
    ), 'thread.__version__ is not a semver'
