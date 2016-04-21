#!/usr/bin/env python
# encoding: utf-8

"""
Assignment 19
Task 1 Program: Using pandas to interact with the amniote database
Jessie Salter
18 April 2016
"""

import argparse
import pandas as pd
import numpy as np


def parser():
    '''Takes user input'''
    parser = argparse.ArgumentParser(
        description="Gets the infile name and list of parameters")
    parser.add_argument(
        "--infile",
        required=True,
        help="Enter the name of the input file",
        type=str
        )
    parser.add_argument(
        "--parameters",
        required=True,
        help="Enter name of file with search parameters sep by line breaks",
        type=str
        )
    parser.add_argument(
        "--outfile",
        required=True,
        help="Enter the name of the outfile you want to create",
        type=str
        )
    return parser.parse_args()


def import_file(infile):
    '''Reads the given file into a pandas dataframe and replaces missing data
    fields with NaN'''
    raw_df = pd.read_csv(infile)
    clean_df = raw_df.replace(-999, np.nan)
    return clean_df


def parameters(input_file):
    '''Reads in user list of parameters and formats into a list'''
    with open(input_file, 'r') as infile:
        read_list = infile.read()
        param_list = read_list.split('\n')
        param_list = list(filter(None, param_list))
        return param_list


def all_stats(df, parameters):
    '''Calculates all stats across all parameters in all orders.'''
    order_dict = dict()
    stats_list = []
    # Can't use the .unique() method because 'class' is a defined variable:
    classes = set(df['class'])
    for param in parameters:
        for tax_class in classes:
            # This iterates over all orders in the set for each class:
            for order in set(df[df['class'] == tax_class]['order']):
                order_dict['class'] = tax_class
                order_dict['order'] = order
                order_dict['parameter'] = param
                order_dict['mean'] = df[df['order'] == order][param].mean()
                # Use stdev to find the 95CI:
                std = df[df['order'] == order][param].std()
                # 95CI is stdev divided by the sqrt of the number of items in
                # your list (# of entries for an order), multiplied by two:
                order_dict['95CI'] = (
                    std/np.sqrt(len(df[df['class'] == tax_class]['order'])))*2
                order_dict['min'] = df[df['order'] == order][param].min()
                order_dict['max'] = df[df['order'] == order][param].max()
                order_dict['median'] = df[df['order'] == order][param].median()
                stats_list.append(order_dict.copy())
    final = pd.DataFrame(stats_list)
    # This puts the columns in the right order:
    final = final[[
        'class', 'order', 'parameter', 'mean', '95CI', 'min', 'max', 'median'
        ]]
    return final


def outfile_writer(final, output):
    '''Writes the dataframe to a csv file'''
    final.to_csv(output)


def main():
    args = parser()
    df = import_file(args.infile)
    params = parameters(args.parameters)
    stats = all_stats(df, params)
    outfile_writer(stats, args.outfile)

if __name__ == '__main__':
    main()
