#! /usr/bin/env python
# encoding: utf-8

'''
Grace Cagle
Assignment 19

Takes a csv file, list of parameters, and output file from the user. Summarizes
the parameters by *order* the parameters, and outputs a csv file with the data
in this format:

class,order,parameter,mean(parameter),95CI(parameter),min(parameter),max(parameter),median(parameter)
Aves,Accipitriformes,female_maturity_d,xxx,yyy,zzz,qqq,sss
'''

import argparse
import pandas as pd
import numpy as np
from scipy import stats
import csv
import math


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', "--infile",
        required=True,
        help="The input file in CSV format"
    )
    parser.add_argument(
        '-o', "--output",
        required=True,
        help="The output file name"
    )
    parser.add_argument(
        '-p', "--parameters",
        required=True,
        help='The paramters to be summarized, matching column names. Please enter like this "female_maturity_d litter_or_clutch_size_n litters_or_clutches_per_y adult_body_mass_g maximum_longevity_y longevity_y female_body_mass_g male_body_mass_g"'''
    )
    return parser.parse_args()


def sort_by_order(args):
    '''Returns a dictionary containing dfs of the different orders. The name
    of the order is the key'''
    orders = dict()
    df = pd.read_csv(args.infile, na_values='-999')
    value_list = list(np.unique(df['order']))
    for v in value_list:
        new_df = df[df['order']==v] # make df of each order
        orders[v] = new_df # set up dictionary {order: df}
    return orders, value_list


def get_data(args, value_list, orders):
    with open(args.output, 'w') as f:
        writer = csv.writer(f)
        parameters = args.parameters.split(' ')
        for value in value_list:
            df = orders[value] # access df in dictionary
            df_class = df.iloc[0,0] # get class info from df
            for param in parameters: #assign parameters to analyze
                series = df[param]
                mean = series.mean()
                minimum = series.min()
                maximum = series.max()
                sample_95ci = 1.96 * stats.sem(series, nan_policy='omit')
                data = [df_class, value, param, mean, minimum, maximum, sample_95ci]
                writer.writerow(data)



def main():
    args = get_args()
    orders, value_list = sort_by_order(args)
    data = get_data(args, value_list, orders)


if __name__ == '__main__':
    main()
