# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BIOL7800 assignment 19
Oscar Johnson 18 April 2016

Copyright Oscar Johnson 2016

provide input txt file of amniote life history database
returns statistics in csv file

input should be in the form of the column headers that
you want statistics for,
divided by commas and with no spaces in between
"""

import os
import pdb
import csv
import argparse
import pandas as pd
import numpy as np


def get_args():
    parser = argparse.ArgumentParser(
            description="""analyze parameters for amniotes""")
    parser.add_argument('--file',
                        type=str,
                        required=True,
                        help="text file to use for analysis",
                        )
    parser.add_argument('--parameters',
                        type=str,
                        required=True,
                        help="enter list of parameters separated by commas",
                        )
    return parser.parse_args()


def amniote(args):
    """
    parses input pandas DataFrame and returns
    various statistics
    writes these to a csv file
    """
    pars = ['class', 'order', 'parameter', 'mean(parameter)',
            '95CI(parameter)', 'min(parameter)', 'max(parameter)',
            'median(parameter)']
    # import file
    df = pd.read_csv(args.file)
    df = df.replace(-999, np.nan)
    # sets of classes and orders
    classes = set(df['class'])
    order = set(df['order'])
    # pdb.set_trace()
    with open('results.csv', 'w') as outfile:
        writer = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(pars)
        for tax in classes:
            div_by_class = df[(df['class'] == tax)]
            # pdb.set_trace()
            # print(div_by_class['order'])
            for taxon in order:
                # pdb.set_trace()
                if taxon in set(list(div_by_class['order'])):
                    # pdb.set_trace()
                    div = div_by_class[(div_by_class['order'] == taxon)]
                    # pdb.set_trace()
                    for val in args.parameters:
                        # pdb.set_trace()
                        r = list(div[val].describe())
                        info = [tax, taxon, val]
                        out_list = info + [str(r[1]), str((r[2]*2)), str(r[3]),
                                           str(r[7]), str(r[5])]
                        # pdb.set_trace()
                        writer.writerow(out_list)


def main():
    args = get_args()
    os.chdir(os.path.dirname(args.file))
    args.parameters = args.parameters.split(',')
    # pdb.set_trace()
    amniote(args)

if __name__ == '__main__':
    main()
