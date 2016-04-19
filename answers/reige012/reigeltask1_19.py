#!/usr/bin/env python
# encoding: utf-8

"""
This program doesn't completely work. I had to give up on it at some point :(
Sorry. 

Edited by Alicia Reigel. 15 April 2016.
Copyright Alicia Reigel. Louisiana State University. 15 April 2016. All
rights reserved.

"""


import numpy
import pandas as pd
import argparse


def parser_get_args():
    """Collect the path to the file of species names and name of output file"""
    parser = argparse.ArgumentParser(
        description="""Input the full path to species name file and desired
            output file name"""
        )
    parser.add_argument(
            '--filepath',
            required=True,
            type=str,
            help='Enter the full path to the database.'
        )
    parser.add_argument(
            '--outputfile',
            required=True,
            type=str,
            help='Enter the desired name for the output file. Must end in .csv'
        )
    parser.add_argument(
            '--parameterlist',
            required=True,
            type=str,
            help='Enter the list of parameters you want summarized.'
        )
    return parser.parse_args()


def get_parameter_info(parameter_list, data, outputfile):
    """ function gets the information related to each order"""
    with open(outputfile, 'a') as output:
        orders_list = pd.unique(data.order.ravel())
        # thanks Jon Nations for this little tidbit of a lifesaver
        print(orders_list)
        for order in orders_list:
            for parameter in parameter_list:
                """print(("Class\tOrder\t{}\tMean {}\t95CI {}\tMin {}\tMax {}\tMedian\n").format(parameter))
                output.write(top_line)"""
                print("This doesn't work. I had to give up on it :(")


def main():
    args = parser_get_args()
    output = args.outputfile
    parameters = args.parameterlist
    parameter_list = parameters.replace(',', '').split(' ')
    amniote_data = pd.read_csv(args.filepath)
    amniote_data = amniote_data.replace(-999, numpy.nan)
    get_parameter_info(parameter_list, amniote_data, output)


if __name__ == '__main__':
    main()
