#!/usr/bin/env python
# encoding: utf-8
"""
assignment 19.

Copyright 2016 Mukesh Maharjan. All rights reserved.
"""
import argparse
import csv
import pandas as pd
import numpy as np
import scipy.stats


def calculate(this_order, para, amniote):
    by_type = 'order'
    class_name = amniote[amniote[by_type] == this_order]['class']
    max_ = amniote[amniote[by_type] == this_order][para].max()
    min_ = amniote[amniote[by_type] == this_order][para].min()
    mean_ = amniote[amniote[by_type] == this_order][para].mean()
    median_ = amniote[amniote[by_type] == this_order][para].median()
    std_ = amniote[amniote[by_type] == this_order][para].std()
    CI = scipy.stats.norm.interval(alpha=.95, loc=mean_, scale=std_)
    # CI_value = mean_ - CI[0]
    return class_name, mean_, max_, min_, median_, CI


def read_write(infilename, parameter_file, outfilename):
    amniote = pd.read_csv(infilename)
    orders = set(amniote['order'])
    amniote = amniote.replace(-999, np.nan)
    writefile = open(outfilename, 'w')
    writer = csv.DictWriter(writefile, fieldnames=['class', 'order', 'parameter', 'mean(parameter)',
                                                   '95CI(parameter)', 'min(parameter)', 'max(parameter)', 'median(parameter)'])
    writer.writeheader()
    with open(parameter_file, 'r') as f:
        for parameter in f:
            for this_order in orders:
                para = parameter[:-1]
                class_name, mean_, max_, min_, median_, CI = calculate(this_order, para, amniote)
                writer.writerow({'class': set(class_name).pop(), 'order': this_order, 'parameter': para, 'mean(parameter)': mean_,
                                '95CI(parameter)': CI, 'min(parameter)': min_, 'max(parameter)': max_, 'median(parameter)': median_})


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("input_filename", help="Give the " +
                       "filename of the database file along with extention")
    parse.add_argument("file_of_list_of_parameters", help="Give the .txt" +
                       " file of parameter list along with the extention")
        #I thought it will be easier to give a file than a messy list.
    parse.add_argument("output_filename", help="Give the name of " +
                       "the output file along with extention")
    file = parse.parse_args()

    infilename = file.input_filename
    parameter_file = file.file_of_list_of_parameters
    outfilename = file.output_filename

    read_write(infilename, parameter_file, outfilename)


if __name__ == '__main__':
    main()
