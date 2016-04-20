#!/usr/bin/env python
# utf-8

import numpy as np
import pandas as pd
import argparse


"""
Assignment 19, Task 1

Uses pandas to modify and write out a .csv version of the amniote natural
history database. Requires three different inputs. I suggest copying the column
inputs from the -input_columns 'help' portion.

AMNIOTE DATA URL:

http://esapubs.org/archive/ecol/E096/269/Data_Files/Amniote_Database_Aug_2015.csv

"""


def args_in():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, type=str,
                        help="give input .csv file of Amniote Data. include path if not in folder. alternatively, use the url http://esapubs.org/archive/ecol/E096/269/Data_Files/Amniote_Database_Aug_2015.csv")
    parser.add_argument('-c', '--input_columns', required=True,
                        nargs='+',
                        help="give input columns. Suggested: class\n order\n female_maturity_d\n   litter_or_clutch_size_n\n litters_or_clutches_per_y\n adult_body_mass_g\n maximum_longevity_y\n longevity_y\n female_body_mass_g\n male_body_mass_g")
    parser.add_argument('-o-', '--output', required=True, help='give output file')
    args = parser.parse_args()
    return args


def stack_file(args):
    data = pd.read_csv(args.input)
    data = data.replace(-999, np.nan)
    data = data.replace(-999.00, np.nan)
    data_group = data.groupby('order', as_index=True)
    data_cols = data_group[[args.input_columns]]
    # See suggested columns above
    data_agg = data_cols.agg([np.mean, np.amin, np.amax,
                              np.median, np.std])
    data_stack = data_agg.stack(level=0)
    return data_stack


def main():
    args = args_in()
    data_stack = stack_file(args)
    data_stack.to_csv(args.output)


if __name__ == '__main__':
    main()
