# pcsv_example_5.py
# Copyright (c) 2013-2019 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0111,C0410,W0104

import pmisc, pcsv


def main():
    ctx = pmisc.TmpFile
    with ctx() as ifname:
        with ctx() as ofname:
            # Create first data file
            data = [
                ["Ctrl", "Ref", "Result"],
                [1, 3, 10],
                [1, 4, 20],
                [2, 4, 30],
                [2, 5, 40],
                [3, 5, 50],
            ]
            pcsv.write(ifname, data, append=False)
            # Sort
            pcsv.dsort(
                fname=ifname,
                order=[{"Ctrl": "D"}, {"Ref": "A"}],
                has_header=True,
                ofname=ofname,
            )
            # Verify that resulting file is correct
            ref_data = [[3, 5, 50], [2, 4, 30], [2, 5, 40], [1, 3, 10], [1, 4, 20]]
            obj = pcsv.CsvFile(ofname, has_header=True)
            assert obj.header() == ["Ctrl", "Ref", "Result"]
            assert obj.data() == ref_data


if __name__ == "__main__":
    main()
