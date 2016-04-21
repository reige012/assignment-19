# !/usr/bin/env python
# encoding: utf-8

"""
Assignment 19 task 1 program:
Created by Andre Moncrieff on 11 April 2016.
Copyright 2016 Andre E. Moncrieff. All rights reserved.

Note: the Amniote database must be in the same directory as this program

"""

import argparse
import pandas
import numpy


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inp_name", required=True,
                        help="Enter the file name (including extension) of" +
                        " the amniote natural history database",
                        type=str)
    parser.add_argument("--param_list", required=True, nargs="+",
                        help="Enter parameters you wish to summarize",
                        type=str)
    parser.add_argument("--out_name", required=True,
                        help="Enter the file name (including .csv extension)" +
                        " of the output file", type=str)
    args = parser.parse_args()
    return args


def read_in_csv(inp_name):
    amniote_df = pandas.read_csv(inp_name)
    return amniote_df


def clean_up(amniote_df):
    amniote = amniote_df.replace(-999, numpy.nan)
    return amniote


def unique_orders(df):
    unique_orders = pandas.unique(df.order.ravel())
    return unique_orders

"""
def summarize_data(unique_orders, param_list, df, out_name):
    with open(out_name, "w") as outfile:
        for order in set_of_orders:
            outfile.write(order)
            #for parameter in param_list:
            #    clean_df[order][parameter].describe()

"""


def main():
    args = parser()
    amniote_df = read_in_csv(args.inp_name)
    df = clean_up(amniote_df)
    uniq_ord = unique_orders(df)
    print(uniq_ord)
    # summarize_data(uniq_ord, args.param_list,
    #                clean_df, args.out_name)

    # Ran out of time to finish!!!

if __name__ == '__main__':
    main()
