#!/usr/bin/env python
# encoding: utf-8
"""
created by me for task1
"""
import argparse
import numpy
import pandas as pd


def get_parser():
    """
   using argparse to takes the list  as input
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputfile", required=True)
    parser.add_argument("--listofparameters", required=True, type=list)
    parser.add_argument("--outputfile", required=True)
    args = parser.parse_args()
    return args


def read_file(infile):
    infile = pd.read_csv('Amniote_Database_Aug_2015.csv')
    # print(amniote.info())
    infile = infile.replace(-999, numpy.nan)
    # print(amniote.head())
    # print(amniote.tail(4))
    return infile


def class_parameters(infile, i, order):
    F = infile[infile['order'] == order]['class']
    return F


def mean_parameter(infile, i, order):
    A = infile[infile['order'] == order][i].mean()
    return A


def interval_parameter(infile, i, order):
    B = infile[infile['order'] == order][i].max()
    return B


def min_parameter(infile, i, order):
    C = infile[infile['order'] == order][i].min()
    return C


def max_parameter(infile, i, order):
    D = infile[infile['order'] == order][i].max()
    return D


def median_parameter(infile, i, order):
    E = infile[infile['order'] == order][i].median()
    return E


def main():
    args = get_parser()
    infile = read_file(args.inputfile, "r")
    orders = infile['order'].unique()
    parameters = args.listofparameters
    for i in parameters:
        for order in orders:
            F = class_parameters(infile, i, order)
            print(F)
            A = mean_parameter(infile, i, order)
            print(A)
            B = interval_parameter(infile, i, order)
            print(B)
            C = min_parameter(infile, i, order)
            print(C)
            D = max_parameter(infile, i, order)
            E = median_parameter(infile, i, order)
        my_df = pd.DataFrame({'class': [F], 'order': [order], 'parameter': [i],
                              'mean': [A], 'interval': [B], 'min': [C],
                              'max': [D], 'median': [E]})
    outfile = open(args.outputfile)
    my_df.to_csv(outfile)

if __name__ == '__main__':
    main()
