#!/bin/env python3

import random

if __name__ == '__main__':
    print("Sektion,LV,M,JL")
    for i in range(random.randint(1, 1000)):
        print(f"Sektion-{i},Mond,{random.randint(0, 2000)},{random.randint(0, 100)}")
