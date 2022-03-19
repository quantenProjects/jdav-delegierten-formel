#/bin/env python3

import pandas as pd

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()

    if len(args.files) == 1:
        df = pd.read_csv(args.files[0])
        columns_to_compare = list(filter(lambda x: x.startswith("d_n"), df.columns.values))
        if len(columns_to_compare) == 2:
            print(f"comparing {columns_to_compare}")
            print()
            comparison = df[columns_to_compare[0]].compare(df[columns_to_compare[1]])
            if len(comparison) > 0:
                print(comparison)
            else:
                print("Identical!")
        else:
            raise ValueError(f"Comparison in one file needs exactly two columns starting with d_n")
    elif len(args.files) == 2:
        a = pd.read_csv(args.files[0])
        b = pd.read_csv(args.files[1])
        comparison = a[["Sektion","d_n"]].compare(b[["Sektion","d_n"]])
        if len(comparison) > 0:
            print(comparison)
        else:
            print("Identical!")
    else:
        raise ValueError(f"Comparision of {len(args.files)} files is not supported")
