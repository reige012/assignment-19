# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Marco
# @Date:   2016-04-17 14:40:30
# @Last Modified by:   Marco
# @Last Modified time: 2016-04-18 11:54:18


"""
Created on Sun Apr 17 15:17:17 2016

@author: Marco
"""

import argparse
# import scipy
import numpy
import pandas as pd


def parser_function():
    '''
    Function to parse arguments
    '''
    parser = argparse.ArgumentParser(description='''This program gets a
         text file with species names as input to create a taxonomic query on
         NCBI and retrieve taxonomic levels that have a defined Rank on NCBI
        ''')
    # Adding an argument to 'parse'
    parser.add_argument('in_file', type=str,
                        help='type the name and path of the input csv file')
    parser.add_argument('parameters', type=str,
                        help='path to txt file containing the parameters')
    parser.add_argument('out_file', type=str,
                        help='type the name and path of the output csv file')
    args = parser.parse_args()
    inp = args.in_file
    parameters = args.parameters
    outp = args.out_file
    return inp, parameters, outp


def text_to_list(txt_file):
    parameters = []
    with open(txt_file, 'r') as f:
        for line in f:
            parameters.append(line.strip("\n"))
    return parameters


def ci(df): return df.quantile(q=0.95)


def pivotation(amniotes, parameters):
    mean = pd.pivot_table(amniotes, values=parameters,
                          index=['class', 'order'], aggfunc=numpy.mean)
    mean.insert(0, column="Parameter",
                value="MEAN", allow_duplicates=True)
    minimum = pd.pivot_table(amniotes, values=parameters,
                             index=['class', 'order'], aggfunc=numpy.min)
    minimum.insert(0, column="Parameter",
                   value="MINIMUM", allow_duplicates=True)
    maximum = pd.pivot_table(amniotes, values=parameters,
                             index=['class', 'order'], aggfunc=numpy.max)
    maximum.insert(0, column="Parameter",
                   value="MAXIMUM", allow_duplicates=True)
    median = pd.pivot_table(amniotes, values=parameters,
                            index=['class', 'order'], aggfunc=numpy.median)
    median.insert(0, column="Parameter",
                  value="MEDIAN", allow_duplicates=True)
    ci95 = pd.pivot_table(amniotes, values=parameters,
                          index=['class', 'order'], aggfunc=ci)
    ci95.insert(0, column="Parameter",
                value="CI95", allow_duplicates=True)
    concate = mean.append([minimum, maximum, median, ci95])
    classes = []
    orders = []
    for x in concate.index:
        classes.append(x[0])
        orders.append(x[1])
    concate.insert(0, "Class", classes)
    concate.insert(1, "Order", orders)
    concate['index'] = list(range(len(concate)))
    concate = concate.set_index('index')
    return concate


def main():
    input_csv, parameters, output_csv = parser_function()
    amniotes = pd.read_csv(input_csv)
    amniotes = amniotes.replace(-999, numpy.nan)
    amniotes = amniotes.replace(float(-999), numpy.nan)
    amniotes = amniotes.replace(str(-999), numpy.nan)
    parameters = text_to_list(parameters)
    concate = pivotation(amniotes, parameters)
    concate.to_csv(output_csv)

if __name__ == '__main__':
    main()
