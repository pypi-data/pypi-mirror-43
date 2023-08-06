# pcsv_example_1.py
# Copyright (c) 2013-2019 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0111,C0410,W0104

import pmisc, pcsv


def main():
    with pmisc.TmpFile() as fname:
        ref_data = [["Item", "Cost"], [1, 9.99], [2, 10000], [3, 0.10]]
        # Write reference data to a file
        pcsv.write(fname, ref_data, append=False)
        # Read the data back
        obj = pcsv.CsvFile(fname)
    # After the object creation the I/O is done,
    # can safely remove file (exit context manager)
    # Check that data read is correct
    assert obj.header() == ref_data[0]
    assert obj.data() == ref_data[1:]
    # Add a simple row filter, only look at rows that have
    # values 1 and 3 in the "Items" column
    obj.rfilter = {"Item": [1, 3]}
    assert obj.data(filtered=True) == [ref_data[1], ref_data[3]]


if __name__ == "__main__":
    main()
