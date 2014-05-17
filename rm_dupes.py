import csv
reader = open("authors_copy.csv", "r")
lines = reader.read().split("\n")
reader.close()

writer = open("authors_copy.csv", "w")
for line in set(lines):
    writer.write(line + "\n")
writer.close()
