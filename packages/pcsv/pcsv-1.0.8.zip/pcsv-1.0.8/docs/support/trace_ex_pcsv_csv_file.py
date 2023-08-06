# trace_ex_pcsv_csv_file.py
# Copyright (c) 2013-2019 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0111,W0212

import docs.support.trace_support


def trace_module(no_print=False):
    """Trace pcsv csv_file module exceptions."""
    mname = "csv_file"
    fname = "pcsv"
    module_prefix = "pcsv.{0}.CsvFile.".format(mname)
    callable_names = (
        "__init__",
        "add_rfilter",
        "data",
        "dsort",
        "replace",
        "reset_dfilter",
        "rows",
        "write",
    )
    return docs.support.trace_support.run_trace(
        mname, fname, module_prefix, callable_names, no_print
    )


if __name__ == "__main__":
    trace_module()
