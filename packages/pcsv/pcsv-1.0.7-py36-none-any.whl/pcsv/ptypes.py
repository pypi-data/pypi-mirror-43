# ptypes.py
# Copyright (c) 2013-2019 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0111,C1801,R0916

# PyPI imports
import pexdoc.pcontracts


###
# Global variables
###
_SUFFIX_TUPLE = (
    "y",
    "z",
    "a",
    "f",
    "p",
    "n",
    "u",
    "m",
    " ",
    "k",
    "M",
    "G",
    "T",
    "P",
    "E",
    "Z",
    "Y",
)


###
# Functions
###
def _check_csv_col_filter(obj):
    if (not isinstance(obj, bool)) and (
        (obj is None)
        or isinstance(obj, (str, int))
        or (
            isinstance(obj, list)
            and (len(obj) > 0)
            and all(
                [
                    (isinstance(item, (str, int))) and (not isinstance(item, bool))
                    for item in obj
                ]
            )
        )
    ):
        return False
    return True


def _check_csv_row_filter(obj):
    # pylint: disable=R0911
    if obj is None:
        return 0
    if not isinstance(obj, dict):
        return 1
    if not len(obj):
        return 2
    if any([not (isinstance(col_name, (str, int))) for col_name in obj.keys()]):
        return 1
    for col_name, col_value in obj.items():  # pragma: no branch
        if (
            (not isinstance(obj[col_name], list))
            and (not _isnumber(obj[col_name]))
            and (not isinstance(obj[col_name], str))
        ):
            return 1
        if isinstance(col_value, list):
            for element in col_value:  # pragma: no branch
                if (not _isnumber(element)) and (not isinstance(element, str)):
                    return 1
    return 0


def _homogenize_data_filter(dfilter):
    """
    Make data filter definition consistent.

    Create a tuple where first element is the row filter and the second element
    is the column filter
    """
    if (dfilter is None) or (dfilter == (None, None)) or (dfilter == (None,)):
        dfilter = (None, None)
    if isinstance(dfilter, bool) or (
        not any([isinstance(dfilter, item) for item in [tuple, dict, str, int, list]])
    ):
        dfilter = (2.0, 2.0)
    if isinstance(dfilter, tuple) and (len(dfilter) == 1):
        dfilter = (dfilter[0], None)
    elif isinstance(dfilter, dict):
        dfilter = (dfilter, None)
    elif isinstance(dfilter, (list, str)) or (
        isinstance(dfilter, int) and (not isinstance(dfilter, bool))
    ):
        dfilter = (None, dfilter if isinstance(dfilter, list) else [dfilter])
    elif isinstance(dfilter[0], dict) or (
        (dfilter[0] is None) and (not isinstance(dfilter[1], dict))
    ):
        pass
    else:
        dfilter = (dfilter[1], dfilter[0])
    return dfilter


def _isnumber(obj):
    """Test is object is a number (copied from pmisc module to avoid import loops)."""
    return (
        (obj is not None)
        and (not isinstance(obj, bool))
        and isinstance(obj, (int, float, complex))
    )


@pexdoc.pcontracts.new_contract()
def csv_col_filter(obj):
    r"""
    Validate if an object is a CsvColFilter pseudo-type object.

    :param obj: Object
    :type  obj: any

    :raises:
     * RuntimeError (Argument \`*[argument_name]*\` is not valid). The token
       \*[argument_name]\* is replaced by the *name* of the argument the
       contract is attached to

    :rtype: None
    """
    if _check_csv_col_filter(obj):
        raise ValueError(pexdoc.pcontracts.get_exdesc())


@pexdoc.pcontracts.new_contract()
def csv_col_sort(obj):
    r"""
    Validate if an object is a CsvColSort pseudo-type object.

    :param obj: Object
    :type  obj: any

    :raises:
     * RuntimeError (Argument \`*[argument_name]*\` is not valid). The token
       \*[argument_name]\* is replaced by the *name* of the argument the
       contract is attached to

    :rtype: None
    """
    exdesc = pexdoc.pcontracts.get_exdesc()
    obj = obj if isinstance(obj, list) else [obj]
    if len(obj) == 0:
        raise ValueError(exdesc)
    for item in obj:
        # Weed out items not having the right basic types
        if isinstance(item, bool) or (
            (not isinstance(item, str))
            and (not isinstance(item, int))
            and (not isinstance(item, dict))
        ):
            raise ValueError(exdesc)
        # If it is a dictionary, the key has to be a valid column name and the
        # sort order has to be either 'A' (for ascending) or 'D' (for
        # descending), case insensitive
        if isinstance(item, dict):
            keys = list(item.keys())
            if (len(keys) > 1) or (
                (len(keys) == 1)
                and ((not isinstance(keys[0], int)) and (not isinstance(keys[0], str)))
            ):
                raise ValueError(exdesc)
            value = item[keys[0]]
            if value not in ["A", "D", "a", "d"]:
                raise ValueError(exdesc)


@pexdoc.pcontracts.new_contract()
def csv_data_filter(obj):
    r"""
    Validate if an object is a CsvDataFilter pseudo-type object.

    :param obj: Object
    :type  obj: any

    :raises:
     * RuntimeError (Argument \`*[argument_name]*\` is not valid). The token
       \*[argument_name]\* is replaced by the *name* of the argument the
       contract is attached to

    :rtype: None
    """
    if isinstance(obj, tuple) and len(obj) > 2:
        raise ValueError(pexdoc.pcontracts.get_exdesc())
    obj = _homogenize_data_filter(obj)
    row_value = _check_csv_row_filter(obj[0])
    col_value = _check_csv_col_filter(obj[1])
    if col_value or (row_value != 0):
        raise ValueError(pexdoc.pcontracts.get_exdesc())


@pexdoc.pcontracts.new_contract()
def csv_filtered(obj):
    r"""
    Validate if an object is a CsvFilter pseudo-type object.

    :param obj: Object
    :type  obj: any

    :raises:
     * RuntimeError (Argument \`*[argument_name]*\` is not valid). The token
       \*[argument_name]\* is replaced by the *name* of the argument the
       contract is attached to

    :rtype: None
    """
    if obj in [True, False, "B", "b", "C", "c", "R", "r", "N", "n"]:
        return None
    raise ValueError(pexdoc.pcontracts.get_exdesc())


@pexdoc.pcontracts.new_contract(
    argument_invalid="Argument `*[argument_name]*` is not valid",
    argument_empty=(ValueError, "Argument `*[argument_name]*` is empty"),
)
def csv_row_filter(obj):
    r"""
    Validate if an object is a CsvRowFilter pseudo-type object.

    :param obj: Object
    :type  obj: any

    :raises:
     * RuntimeError (Argument \`*[argument_name]*\` is not valid). The token
       \*[argument_name]\* is replaced by the *name* of the argument the
       contract is attached to

     * ValueError (Argument \`*[argument_name]*\` is empty). The token
       \*[argument_name]\* is replaced by the *name* of the argument the
       contract is attached to

    :rtype: None
    """
    exdesc = pexdoc.pcontracts.get_exdesc()
    ecode = _check_csv_row_filter(obj)
    if ecode == 1:
        raise ValueError(exdesc["argument_invalid"])
    if ecode == 2:
        raise ValueError(exdesc["argument_empty"])
