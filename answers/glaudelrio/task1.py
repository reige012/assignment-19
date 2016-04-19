# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 19:33:54 2016

@author: Glaucia
"""

import argparse
import pandas as pd
import numpy


def arguments():
    """"parsing arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help="add input file and entire path don't use flags")
    parser.add_argument('output_name', type=str, help="add input file name and path right after input path")
    parser.add_argument('parameters', type=str, help="add path and parameters file name")
    args = parser.parse_args()
    input_file = args.input_file
    output_name = args.output_name
    parameters = args.parameters
    return input_file, output_name, parameters


def manipulate_input(inp):
    """manipulates the input csv to deal with missing data"""
    text = pd.read_csv(inp)
    text = text.replace(-999, numpy.nan)
    text = text.replace(float(-999), numpy.nan)
    text = text.replace("-999", numpy.nan)
    return text


def descriptive(data_frame, parameter):
    """calculates the measures for each parameter and creates a data frame"""
    parameterlis = []
    data_frame['new'] = data_frame["order"].map(str) + ',' + data_frame["class"]
    orders = data_frame.new.unique()
    byorder = data_frame.groupby('new')
    mean_ = byorder[parameter].mean()
    minimum = byorder[parameter].min()
    maximum = byorder[parameter].max()
    median = byorder[parameter].median()
    IClower = byorder[parameter].quantile(0.025)
    IClower = dict(IClower)
    IClower = list(IClower.values())
    ICupper = byorder[parameter].quantile(0.975)
    ICupper = dict(ICupper)
    ICupper = list(ICupper.values())
    maximum = dict(maximum)
    maximum = list(maximum.values())
    mean_ = dict(mean_)
    mean_ = list(mean_.values())
    median = dict(median)
    median = list(median.values())
    minimum = dict(minimum)
    minimum = list(minimum.values())
    for i in range(len(orders)):
        parameterlis.append(parameter)
    my_dict = {'Class': orders, 'PARAMETER': parameterlis, 'MEAN': mean_,
               'MINIMUM': minimum, 'MEDIAN': median, 'MAXIMUM': maximum,
               'CI_LOWER': IClower, 'CI_UPPER': ICupper}
    my_df = pd.DataFrame(my_dict, index=list(range(len(orders))))
    new_order = []
    new_class = []
    for value in my_df['Class']:
        new_class.append(value.split(',')[1])
        new_order.append(value.split(',')[0])
    my_df.insert(0, "ORDER", new_class)
    my_df.insert(1, "CLASS", new_order)
    my_df.pop('Class')
    df = my_df[['CLASS', 'ORDER', 'PARAMETER', 'MEAN', 'CI_LOWER',
                'CI_UPPER', 'MINIMUM', 'MAXIMUM', 'MEDIAN']]
    return df


def text_to_list(parameters_file):
    """deals with a list of parameter (input)"""
    parameters = []
    with open(parameters_file, 'r') as file:
        for line in file:
            parameters.append(line.strip("\n"))
    return parameters


def several_parameters(text, parameters):
    """concatenate each data frame for each parameter"""
    frames = []
    for parameter in parameters:
        parameter_df = descriptive(text, parameter)
        frames.append(parameter_df)
    result = pd.concat(frames)
    return result


def main():
    inp, out, parameters_file = arguments()
    amniote = manipulate_input(inp)
    parameters = text_to_list(parameters_file)
    final_df = several_parameters(amniote, parameters)
    final_df.to_csv(out)


if __name__ == '__main__':
    main()
