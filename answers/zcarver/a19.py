#! /usr/bin/env python
# encoding UTF-8

'''
Assignment19Task1 biol7800
ZacCarver 04/19/2016
class,order,parameter,mean(parameter),95CI(parameter),min(parameter),max(parameter),median(parameter)
Aves,Accipitriformes,female_maturity_d,xxx,yyy,zzz,qqq,sss
a mess that was unfortunately not finished joy.
'''

import argparse
import numpy
import pandas as pd
#import scipy
#import scikits.bootsrap as bootstrap


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile", type=str,
                        help="provide history csv file")
    parser.add_argument("--listofparameters")
    #parser.add_argument("outfile", type=str,
                        #help="provide csv file name for results")
    return parser.parse_args()


def mean(amniote, parameter, c, o):
    for a in amniote[amniote[['class']==c]['order']==o]:
        mean = a[parameter].mean()
        mn = a[parameter].min()
        mx = a[parameter].max()
        median = a[parameter].median()
    return a, parameter, mean, mn, mx, median


'''def paras(amniote, order, parameter):
    #print(order)
    orda = amniote[amniote['order']==order][parameter].describe()
    print(order, '\n', orda)'''


def main():
    arg = args()
    amniote = pd.read_csv(arg.infile)
    amniote = amniote.replace(-999, numpy.nan)
    #order = amniote.order.unique()
    parameters = pd.read_csv(arg.listofparameters)
    for parameter in parameters:
        for c in pd.unique(amniote['class']):
            for o in pd.unique(amniote['order']):
                #print(parameter)
                #paras(amniote, order, parameter)
                mean_p = mean(amniote, parameter, c, o)
                #mx_p = mx(amniote, parameter, o)
                #median_p = median(amniote, parameter, o)
                print(mean_p)
                #print(pd.unique(amniote.columns.ravel()))
                #print(pd.unique(amniote['class']))
                #write csv with header something like class,order,parameter,mean(parameter),95CI(parameter),min(parameter),max(parameter),median(parameter)
if __name__ == '__main__':
    main()
