#!/usr/bin/env python
# encoding: utf-8

import pandas
import numpy as np
import argparse

"""
My 1st task for assignment 19
I worked with AJ dun dun dun
Created by Michael Henson on 18 April 2016.
Copyright 2016 Michael W Henson. All rights reserved.

"""


def askingforfiles():
    parser = argparse.ArgumentParser(
        description="give me input, parameters, and output file name")
    parser.add_argument(
        "--I",
        required=True,
        help="Provide the desired .csv file with attributes",
        type=str
    )
    parser.add_argument(
        "--P",
        required=True,
        help="Provide the parameters you wish to find",
        type=str
    )
    parser.add_argument(
        "--O",
        required=True,
        help="Provide the output file name",
        type=str
    )
    return parser.parse_args()


def converting(inputs):
    converted = inputs.replace(-999, np.nan)
    converted = converted.replace(-999.00, np.nan)
    return converted


def dataframing(inputs, csv_P):
    inputs = inputs.groupby(['order', 'class'], as_index=True)
    with open(csv_P) as parms:
        parms = [line.rstrip('\n') for line in parms]
        z = inputs[parms]
        y = z.aggregate([np.mean, np.amax, np.median, np.amin])
    return y


def CI(inputs, csv_P):
    inputs = inputs.groupby(['order', 'class'], as_index=True)
    with open(csv_P) as parms:
        parms = [line.rstrip('\n') for line in parms]
        z = inputs[parms]
        ci = z.aggregate(lambda x: np.std(x, ddof=1)/np.sqrt(x.count()))
        '''
        http://stackoverflow.com/questions/18039923/standard-error-ignoring-nan-in-pandas-groupby-groups/18042914#18042914
        '''
        ci_stacked = ci.stack(level=0)
        ci_stacked = pandas.DataFrame(ci_stacked)
        ci_stacked.columns = ['95CI']
    return ci_stacked


def rework(data, old):
    data_stacked = data.stack(level=0)
    return data_stacked


def main():
    csv = askingforfiles()
    df = pandas.read_csv(csv.I, header=0)
    converted = converting(df)
    data = dataframing(converted, csv.P)
    who = CI(converted, csv.P)
    dey = rework(data, converted)
    result = pandas.concat([who, dey], axis=1, join_axes=[who.index])
    result = result.rename(columns={'amax': 'max'})
    result = result.rename(columns={'amin': 'min'})
    df_titles = ['mean', '95CI', 'min', 'max', 'median']
    result = result.reindex(columns=df_titles)
    '''
    http://chrisalbon.com/python/pandas_dataframe_reindexing.html
    '''
    result.to_csv(csv.O)
    '''
    who dey who dey who dey think goin to beat 'dem bangles....NO BODY!
    '''


if __name__ == '__main__':
    main()
