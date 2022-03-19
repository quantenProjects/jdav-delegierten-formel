#!/bin/env python3

# CC-0

import numpy as np
import pandas as pd

import argparse
from typing import Optional


def calculate_table(input_data : pd.DataFrame, D : int, lv : Optional[str], verbose : bool) -> pd.DataFrame:
    if verbose:
        print(f"input {len(input_data.index)} rows")
    if lv is not None:
        if verbose:
            print(f"now filter for {lv}")
        data = input_data[input_data["LV"] == lv].copy()
        if verbose:
            print(f"after filtering {len(data.index)} rows")
    else:
        data = input_data.copy()

    # calc square root of M
    data["M_SQRT"] = data["M"] ** 0.5

    k = len(data.index)  # number of Sektionen
    JL_gesamt = data["JL"].sum()
    M_SQRT_gesamt = data["M_SQRT"].sum()
    if verbose:
        print()
        print(f"k:               {k}")
        print(f"JL_gesamt:       {JL_gesamt}")
        print(f"M_SQRT_gesamt: {M_SQRT_gesamt}")

    if D < k:
        raise ValueError("D is smaller than k. This isn't allowed!")

    data["d_n"] = np.floor((
                            1 + 0.5 * (D - k) * (data["JL"] / JL_gesamt + data["M_SQRT"] / M_SQRT_gesamt)
                            ) + 0.5 ).astype("uint32")  # floor with +0.5 is "kaufmännisch Runden"

    if verbose:
        print()
        sum_of_delegates = data['d_n'].sum()
        print(f"Sum of delegates {sum_of_delegates}")
        print(f"difference from target size: {sum_of_delegates - D}")
        print()
        print(data)

    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("d", help="the target size D", type=int)
    parser.add_argument("input_file", help="csv file for input")
    parser.add_argument("output_file", help="csv file for output")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("-l", "--lv", help="filter for LV")
    args = parser.parse_args()

    input_df = pd.read_csv(args.input_file)
    output_df = calculate_table(input_df, args.d, args.lv, args.verbose)
    output_df.to_csv(args.output_file)
