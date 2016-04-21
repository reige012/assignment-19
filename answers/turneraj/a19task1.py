#!/usr/bin/env python
# encoding: utf-8

"""
My first task for Assignment 19.

Created by A.J. Turner on April 16, 2016
Copyright 2016 A.J. Turner. All rights reserved. Collaboration/helpful hints
provided by Mikey Henson.
Info on excluding NaN for CI:
http://stackoverflow.com/questions/18039923/\
standard-error-ignoring-nan-in-pandas-groupby-groups/18042914#18042914
"""

import pandas
import argparse
import numpy as np


def file_info():
    """input file, parameters needed, and output file"""
    parser = argparse.ArgumentParser()
    # drop in amniote file to commandline
    parser.add_argument("--infile", help="name of input file. easiest to drag \
    and drop file into commandline", type=str)
    # name file and include .csv at end
    parser.add_argument("--out", help="name of output file you made \
    <name_of_file.csv>", type=str)
    # drop in file "params_file.text" to commandline to get necessary params
    parser.add_argument("--para", help="parameters needed from para_file \
    easiest to drag and drop in file called para_file.txt", type=str)
    return parser.parse_args()


def clean_data(csv):
    csv = csv.replace(-999, np.nan).replace(-999.00, np.nan)
    return csv


def database(myfile, myfile_para):
    index = myfile.groupby(['order', 'class'], as_index=True)
    with open(myfile_para) as parameters:
        parameters = [line.rstrip('\n') for line in parameters]
        params = index[parameters]
        calc = params.agg([np.mean, np.amin, np.amax, np.median])
    return calc


def calc_CI(myfile, myfile_para):
    myfile = myfile.groupby(['order', 'class'], as_index=True)
    with open(myfile_para) as parameters:
        parameters = [line.rstrip('\n') for line in parameters]
        params = myfile[parameters]
        conf_int = params.aggregate(lambda x: np.std(x) / x.count() * 1.96)
        stacking = conf_int.stack(level=0)
        stacking = pandas.DataFrame(stacking)
        stacking.columns = ['95CI']
        # print(stacking) # look at output to see if stacking worked
    return stacking


def combine(data, clean):
    stacking = data.stack(level=0)
    return stacking


def main():
    myfile = file_info()
    csv = pandas.read_csv(myfile.infile, header=0)
    clean = clean_data(csv)
    data = database(clean, myfile.para)
    # print(data) check to see if proper info included in dataframe
    # changing np.amin name to min
    data = data.rename(columns={'amin': 'min'})
    # changing np.amax name to max
    data = data.rename(columns={'amax': 'max'})
    ci = calc_CI(clean, myfile.para)
    stacks = combine(data, clean)
    answer = pandas.concat([ci, stacks], axis=1, join_axes=[ci.index])
    # print(answer) #check to see of two dataframes were joined together
    df_titles = ['mean', '95CI', 'min', 'max', 'median']
    # formatting order of the column headers
    # from: http://chrisalbon.com/python/pandas_dataframe_reindexing.html
    result = answer.reindex(columns=df_titles)
    result.to_csv(myfile.out)


if __name__ == '__main__':
    main()
