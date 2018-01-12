import csv

new_rows = []

with open('data/lapTimes.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONE)
    for row in reader:
        del row[4]
        new_rows.append(row)

with open('data/lapTimes-ms.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(new_rows)
