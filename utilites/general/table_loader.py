import os
import csv


def get_table(tableName):
    currentPath = os.path.dirname(__file__)
    newPath = os.path.join(currentPath, ".\\lookup_tables\\" + tableName)
    lookupTable = csv.reader(open(newPath, "r"), delimiter=",")

    table = []
    for row in lookupTable:
        table.append(row)

    return table
