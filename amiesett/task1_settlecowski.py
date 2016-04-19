#!/usr/bin/env python
# encoding: utf-8
"""
BIOL7800 Assignment 19 Task 1

Amie Settlecowski
19 Apr. 2016

This program summarizes specified attributes (parameters) of the amniote
natural history database by order and outputs the summary to a csv file.

python ../task1_settlecowski.py --i ../pathto/input.csv --o output.csv
--p parameters
"""
import argparse
import os

import pandas
import numpy
from scipy import stats


def get_args(parserr):
    '''
    Requires --i flag for user to specify path to input file
    Requires --o flag for user to name output file
    '''
    parserr.add_argument("--i",
        required=True,
        help="Path to input file",
        type=str)

    parserr.add_argument("--o",
        required=True,
        help="Name output file",
        type=str)

    parserr.add_argument("--p",
        required=True,
        help="Choose parameters to summarize (separate by spaces)",
        type=str,
        nargs='+')


def get_data(in_file, parameters):
    labels = ['class', 'order']
    keep = labels + parameters
    dataframe = pandas.read_csv(in_file, usecols=keep)
    dataframe = dataframe.replace('-999', numpy.nan)
    return dataframe


def summarize_parameter(dataframe, clas, order, parameter):
    summary = {}
    summary['order'] = order
    summary['class'] = clas
    summary['parameter'] = parameter
    data = dataframe[dataframe['order'] == order][parameter]
    summary['mean'] = data.mean()
    summary['maximum'] = data.max()
    summary['minimum'] = data.min()
    summary['median'] = data.median()
    ci = construct_CI(len(data), stats.sem(data), summary['mean'])
    summary['CI_lower'] = ci[0]
    summary['CI_upper'] = ci[1]
    return summary


def construct_CI(n, sem, mean):
    if n >= 30:
        return stats.norm.interval(0.95, loc=mean, scale=sem)
    else:
        return stats.t.interval(0.95, (n-1), loc=mean, scale=sem)


def write_line(dict, ofile):
    '''Writes one line of csv file for each parameter per order'''
    headers = ['class', 'order', 'parameter', 'mean', 'CI_lower', 'CI_upper', 'maximum', 'minimum', 'median']
    for h in headers:
        ofile.write('{},'.format(dict[h]))
    ofile.write('\n')


def main():
    # Create Parser with arguments for input species and output file
    parser = argparse.ArgumentParser()
    get_args(parser)
    args = parser.parse_args()

    # Change to directory with input file
    working_dir = os.path.split(args.i)[0]
    os.chdir(working_dir)

    # Parse input csv file to working dataframe
    amniote = get_data(args.i, args.p)
    # Create list of orders to summarize
    orders = set(tuple(amniote['order']))
    with open(args.o, 'w') as out_file:
        # Write header line to csv file
        out_file.write('class,order,parameter,mean,CI_lower,CI_upper,maximum,minimum,median\n')
        # Summarize every order iteratively
        for order in orders:
            clas = amniote[amniote['order'] == order]['class'].iloc[0]
            # Summarize every specified parameter iteratively for each order
            for parameter in args.p:
                p_dict = summarize_parameter(amniote, clas, order, parameter)
                write_line(p_dict, out_file)

if __name__ == '__main__':
    main()
