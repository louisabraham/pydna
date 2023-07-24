#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2013-2023 by Björn Johansson.  All rights reserved.
# This code is part of the Python-dna distribution and governed by its
# license.  Please see the LICENSE.txt file that should have been included
# as part of this package.


from operator import itemgetter as _itemgetter

from pydivsufsort import common_substrings as _common_substrings


def common_sub_strings(stringx: str, stringy: str, limit=25):
    """Finds all common substrings between stringx and stringy
    longer than limit. This function is case sensitive.
    The substrings may overlap.

    returns a list of tuples describing the substrings
    The list is sorted longest -> shortest.

    Parameters
    ----------
    stringx : str
    stringy : str
    limit : int, optional

    Returns
    -------
    list of tuple
        [(startx1, starty1, length1),(startx2, starty2, length2), ...]

        startx1 = startposition in x, where substring 1 starts
        starty1 = position in y where substring 1 starts
        length1 = lenght of substring


    Examples
    --------

    >>> from pydna.common_sub_strings import common_sub_strings
    >>> common_sub_strings("gatgatttcggtagtta", "gtcagtatgtctatctatcgcg", limit=3)
    [(1, 6, 3), (7, 17, 3), (10, 4, 3), (12, 3, 3)]

    ::

        Overlaps   Symbols
        (1, 6,  3)   ---
        (7, 17, 3)   +++
        (10, 4, 3)   ...
        (12, 3, 3)   ===


                    ===
        gatgatttcggtagtta           stringx
         ---   +++...

            ...
        gtcagtatgtctatctatcgcg      stringy
           ===---        +++

    """
    match = _common_substrings(stringx, stringy, limit)
    match.sort(key=_itemgetter(2), reverse=True)
    return match


def terminal_overlap(stringx: str, stringy: str, limit=15):
    """Finds the the flanking common substrings between stringx and stringy
    longer than limit. This means that the results only contains substrings
    that starts or ends at the the ends of stringx and stringy.

    This function is case sensitive.

    returns a list of tuples describing the substrings
    The list is sorted longest -> shortest.

    Parameters
    ----------
    stringx : str
    stringy : str
    limit : int, optional

    Returns
    -------
    list of tuple
        [(startx1,starty1,length1),(startx2,starty2,length2), ...]

        startx1 = startposition in x, where substring 1 starts
        starty1 = position in y where substring 1 starts
        length1 = lenght of substring


    Examples
    --------

    >>> from pydna.common_sub_strings import terminal_overlap
    >>> terminal_overlap("agctatgtatcttgcatcgta", "gcatcgtagtctatttgcttac", limit=8)
    [(13, 0, 8)]

    ::

                        <-- 8 ->
           <---- 13 --->
           agctatgtatcttgcatcgta                    stringx
                        gcatcgtagtctatttgcttac      stringy
                        0

    """
    return [
        m
        for m in common_sub_strings(stringx, stringy, limit)
        if (m[0] == 0 and m[1] + m[2] == len(stringy))
        or (m[1] == 0 and m[0] + m[2] == len(stringx))
    ]


if __name__ == "__main__":
    import os as _os

    cached = _os.getenv("pydna_cached_funcs", "")
    _os.environ["pydna_cached_funcs"] = ""
    import doctest

    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
    _os.environ["pydna_cached_funcs"] = cached
