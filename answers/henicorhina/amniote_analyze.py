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
import argparse
import pandas as pd


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
    df = pd.read_csv(args.file)
    


def main():
    args = get_args()
    # rename outfile to .fasta if needed
    if args.out_file[-4:] != '.csv':
        args.out_file += '.csv'
    else:
        pass
    os.chdir(os.path.dirname(args.file))
    amniotes(args)
    l = [class,order,parameter,mean(parameter),
        95CI(parameter),min(parameter),max(parameter),median(parameter)]

if __name__ == '__main__':
    main()
