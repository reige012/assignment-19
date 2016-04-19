# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BIOL7800 assignment 19
Oscar Johnson 18 April 2016

Copyright Oscar Johnson 2016

provide input txt file of amniote life history database
returns NCBI taxonomy as csv file
"""

import os
import pdb
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

    """
    # import file
    df = pd.read_csv(args.file)
    df = df.replace(-999, np.nan)
    # sets of classes and orders
    classes = set(df['class'])
    order = set(df['order'])
    # l = df[(df['class']=='Aves')]
    outfile = open('results.csv', 'w')
    for tax in classes:
        div_by_class = df[(df['class']==tax)]
        # pdb.set_trace()
        for taxon in order:
            if taxon in div_by_class['order']:
                div_by_order = div_by_class[(div_by_class['order']==taxon)]
                # print(div_by_order)
                for p in args.parameters:
                    r = list(div_by_order[p].describe())
                    info = [tax, taxon, p]
                    out_list = info + [r[1], (r[2]*2), r[3], r[7], r[5]]
                    print(out_list)
                    # div_by_order 
                    outfile.write(out_list, '\n')
    outfile.close()


def main():
    args = get_args()
    os.chdir(os.path.dirname(args.file))
    amniote(args)
    # pars = [class,order,parameter,mean(parameter),
    #     95CI(parameter),min(parameter),max(parameter),median(parameter)]

if __name__ == '__main__':
    main()
