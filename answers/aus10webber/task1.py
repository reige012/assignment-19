#!/usr/bin/env python
# utf-8

"""
BIOL 7800 Assignment 19, Task 1
Austen T. Webber
2016_4_19
"""

import argparse
import numpy as np
import pandas


def askingforfiles():
    parser = argparse.ArgumentParser(
        description="Get files and directories")
    parser.add_argument(
        "--file",
        required=True,
        help="Path for input .csv file",
        type=str
    )
    parser.add_argument(
        "--outdir",
        required=True,
        help="Provide path and name of output file including .csv at the end",
        type=str
    )
    parser.add_argument(
        "--stats",
        required=True,
        help="Which statistics do you want to calculate",
        type=str
    )
    return parser.parse_args()


def replacer(inputs):
    replaced = inputs.replace(-999, np.nan)
    replaced = replaced.replace(-999.00, np.nan)
    return replaced


def dataframing(inputs, path_stats):
    inputs = inputs.groupby(['order', 'class'], as_index=True)
    with open(path_stats) as parms:
        parms = [line.rstrip('\n') for line in parms]
        z = inputs[parms]
        y = z.aggregate([np.mean, np.amax, np.median, np.amin])
    return y


def CI(inputs, path_stats):
    inputs = inputs.groupby(['order', 'class'], as_index=True)
    with open(path_stats) as parms:
        parms = [line.rstrip('\n') for line in parms]
        z = inputs[parms]
        ci = z.aggregate(lambda x: np.std(x, ddof=1)/np.sqrt(x.count()))
        ci_stacked = ci.stack(level=0)
        ci_stacked = pandas.DataFrame(ci_stacked)
        ci_stacked.columns = ['95CI']
    return ci_stacked


def rework(newdf, old):
    newdf_order = newdf.stack(level=0)
    return newdf_order


def main():
    path = askingforfiles()
    df = pandas.read_csv(path.file, header=0)
    replaced = replacer(df)
    newdf = dataframing(replaced, path.stats)
    con = CI(replaced, path.stats)
    fi = rework(newdf, replaced)
    finaldf = pandas.concat([con, fi], axis=1, join_axes=[con.index])
    finaldf.to_csv(path.outdir)


if __name__ == '__main__':
    main()

# http://stackoverflow.com/questions/18039923/standard-error-ignoring-nan-in-pandas-groupby-groups/18042914#18042914
# http://www.randalolson.com/2012/08/06/statistical-analysis-made-easy-in-python/
# http://stackoverflow.com/questions/15033511/compute-a-confidence-interval-from-sample-data
# Thank you to M.W. Henson for helping me calculate 95% CI.
