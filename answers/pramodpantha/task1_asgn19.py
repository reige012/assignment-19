#!/usr/bin/env python
# utf-8


"""
task 1 of assignment 19
http://pandas.pydata.org/pandas-docs/version/0.15.2/tutorials.html
https://docs.python.org/3/library/csv.html
http://hamelg.blogspot.com/2015/11/python-for-data-analysis-part-23-point.html
class slide
"""


import pandas as pd
import numpy as np
import scipy.stats
import math
import argparse
import csv


def get95CI(data):
    z_critical = scipy.stats.norm.ppf(q=0.95)
    finite_vals = data[np.isfinite(data)]
    std_val = finite_vals.std()
    sample_size = len(finite_vals)
    if sample_size == 0:
        margin_of_error = 0
    else:
        margin_of_error = z_critical * (std_val/math.sqrt(sample_size))
    return margin_of_error


def save_output(amniote, unique_orders, parameter_list, filename):
    f = csv.writer(open(filename, 'w'))
    f.writerow(['class', 'order', 'parameter', 'val_95CI(parameter)', 'min_val(parameter)', 'max_val(parameter)', 'mean_val(parameter)', 'median_val(parameter)'])
    for parameter in parameter_list:
        for order_name in unique_orders:
            class_name = amniote[amniote['order'] == order_name]['class'].unique()
            max_val = amniote[amniote['order'] == order_name][parameter].max()
            min_val = amniote[amniote['order'] == order_name][parameter].min()
            mean_val = amniote[amniote['order'] == order_name][parameter].mean()
            median_val = amniote[amniote['order'] == order_name][parameter].median()
            val_95CI = get95CI(amniote[amniote['order'] == order_name][parameter])
            f.writerow([class_name[0], order_name, parameter, val_95CI, min_val, max_val, mean_val, median_val])


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("infile", help="give name of your orderlist")
    parse.add_argument("outfile", help="give your output file name")
    parse.add_argument('-l', '--list', help='delimated list input', type=str)
    args = parse.parse_args()
    # give infile Amniote_Database_Aug_2015.csv
    # give outfile name out
    # give list of parameter as follows:
    # -l female_maturity_d,litter_or_clutch_size_n,litters_or_clutches_per_y,
    # adult_body_mass_g,maximum_longevity_y,longevity_y,female_body_mass_g,
    # male_body_mass_g
    parameter_list = [(item) for item in args.list.split(',')]
    filename = open(args.infile, 'r')
    amniote = pd.read_csv(filename)
    unique_orders = amniote['order'].unique()
    amniote = amniote.replace(-999, np.nan)
    out_filename = 'out.txt '
    save_output(amniote, unique_orders, parameter_list, out_filename)

if __name__ == '__main__':
    main()
