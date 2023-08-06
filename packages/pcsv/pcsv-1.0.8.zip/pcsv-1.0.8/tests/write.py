# write.py
# Copyright (c) 2013-2019 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0103,C0111,C0302,C0413,E0611,F0401,R0201,R0915,W0232

# Standard library imports
import os
import sys

if sys.hexversion >= 0x03000000:
    import unittest.mock as mock
# PyPI imports
import pmisc
from pmisc import AE, AI
import pytest

if sys.hexversion < 0x03000000:
    import mock
# Intra-package imports
import pcsv

if sys.hexversion < 0x03000000:
    from pcsv.compat2 import _read
else:
    from pcsv.compat3 import _read


###
# Test functions
###
@pytest.mark.write
def test_write_function_exceptions():
    """Test write() function raises right exceptions."""
    obj = pcsv.write
    some_fname = os.path.join(os.path.abspath(os.sep), "some", "file")

    def mock_make_dir_io(fname):
        raise IOError(
            "File {0} could not be created".format(fname), "Permission denied"
        )

    def mock_make_dir_os(fname):
        raise OSError(
            "File {0} could not be created".format(fname), "Permission denied"
        )

    some_fname = os.path.join(os.path.abspath(os.sep), "some", "file")
    data = [["Col1", "Col2"], [1, 2]]
    AI(obj, "fname", fname=5, data=data)
    AI(obj, "append", fname=some_fname, data=data, append="a")
    exmsg = "File {0} could not be created: Permission denied".format(some_fname)
    with mock.patch("pmisc.make_dir", side_effect=mock_make_dir_io):
        AE(obj, OSError, exmsg, fname=some_fname, data=data)
    with mock.patch("pmisc.make_dir", side_effect=mock_make_dir_os):
        AE(obj, OSError, exmsg, fname=some_fname, data=data)
    AI(obj, "data", fname="test.csv", data=[True, False])
    exmsg = "There is no data to save to file"
    AE(obj, ValueError, exmsg, fname="test.csv", data=[[]])


def test_write_function_works():
    """Test if write() method behaves properly."""
    lsep = "\r\n"
    with pmisc.TmpFile() as fname:
        pcsv.write(fname, [["Input", "Output"], [1, 2], [3, 4]], append=False)
        written_data = _read(fname)
    assert written_data == "Input,Output{0}1,2{0}3,4{0}".format(lsep)
    with pmisc.TmpFile() as fname:
        pcsv.write(fname, [["Input", "Output"], [1, 2], [3, 4]], append=False)
        pcsv.write(fname, [[5.0, 10]], append=True)
        written_data = _read(fname)
    assert written_data == "Input,Output{0}1,2{0}3,4{0}5.0,10{0}".format(lsep)
