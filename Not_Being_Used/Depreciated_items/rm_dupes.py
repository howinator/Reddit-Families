# This script removes the duplicates from a copy of the authors.csv files.
# Be sure to make a copy of the authors.csv file so that we don't tamper
# with it.

import csv
reader = open("authors_copy.csv", "r")
lines = reader.read().split("\n")
reader.close()

writer = open("authors_copy.csv", "w")
for line in set(lines):
    writer.write(line + "\n")
writer.close()
