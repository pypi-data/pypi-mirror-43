# -*- coding: utf-8 -*-
"""This script find the minimum value from the vector/list given by user"""

from __future__ import print_function


def find_minimum(input_list):
    """This function first validate the vector/list and then
    find minimum from it"""
    mini = None
    desc_part = []
    asc_part = []
    check = True
    str_list = [x for x in input_list if isinstance(x, str)]

    #Check string is not into list
    if str_list:
        # STRING NOT ALLOWED
        check = False

    # Check input is valid or not
    # 1. Check list length
    if len(input_list) in [0, 1, 2]:
        # LIST LENGTH MUST BE MORE THAN TWO
        check = False
    # 2.Check Desending Part
    if check:
        for i in range(len(input_list)-1):
            if input_list[i] - input_list[i+1] < 0:
                break
            elif input_list[i] - input_list[i+1] == 0:
                # DESC ORDER HAS DUPLICATES
                check = False
            mini = input_list[i +1]
            desc_part = input_list[:i +1]
            asc_part = input_list[i +1:]
        if len(desc_part) == 0:
            # DESC ORDER IS FAILED
            check = False
        # 3. Check Ascending Part
        if len(asc_part) > 1:
            for i in range(len(asc_part)-1):
                if asc_part[i] - asc_part[i+1] > 0:
                    # ASC ORDER IS FAILED
                    check = False
                elif asc_part[i] - asc_part[i+1] == 0:
                    # ASC ORDER HAS DUPLICATES
                    check = False
        else:
            # ASCENDING PART MUST HAS MORE THAN ONE ELEMENT
            check = False
    if check:
        print(" INPUT: ", input_list)
        print(" OUTPUT: ", mini)
    else:
        print(" OUTPUT: INVALID INPUT")
