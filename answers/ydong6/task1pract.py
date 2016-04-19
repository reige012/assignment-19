#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Apr 18, 2016
A19task1
 In the amniote natural history database (task1-files),
there is a large CSV file containing attributes for a number of life history
characteristics of amniotes. Write a program that uses pandas to summarize
attributes of this entire file by order (format below). Write your output to a
CSV file that looks like:

class,order,parameter,mean(parameter),95CI(parameter),min(parameter),max(parameter),median(parameter)
@author: York
'''
import numpy
import pandas as pd
import scipy
#import scikits.bootstrap as bootstrap
import numpy as np
import scipy as sp
import scipy.stats
import argparse


def parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="Enter the path to the input file of species names",
        type=str)
    parser.add_argument(
        "--output",
        required=True,
        help="Enter the name of the output file",
        type=str)


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1 + confidence) / 2., n - 1)
    outfile.write("95CI: " + str(h))
    return m, m - h, m + h


outfile = open('call.txt', "w+")


def parameter(my_df):
    c = my_df['female_maturity_d'].mean()
    # value_list.append[c]
    # print(value_list)
    print(c)
    outfile.write("mean: " + str(c))
    d = my_df['female_maturity_d'].min()
    print(d)
    outfile.write("min: " + str(d))
    f = my_df['female_maturity_d'].max()
    print(f)
    outfile.write("max: " + str(f))
    g = my_df['female_maturity_d'].median()
    print(g)
    outfile.write("median: " + str(g))
    #CIs = bootstrap.ci(data=my_df, statfunction=scipy.mean)
    # print(CIs)
    return parameter


def main():
    args = parser()
    my_df1 = pd.read_csv(args.input)
    my_df = my_df1.replace(-999, numpy.nan)
    # print(my_df)
    # outfile.write(str(my_df.describe()))
    value_list = ['class', 'order', 'species']
    print(value_list)
    df = my_df[value_list]
    # csv_result=my_df.sort(['order','class','female_maturity_d','species'],ascending=[1,4,3,2])
    outfile.write(str(df))
    # print(df)
    parameter(my_df)
    mean_confidence_interval(my_df)

if __name__ == '__main__':
    main()
