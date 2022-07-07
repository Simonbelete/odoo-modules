import csv
import xmlrpc.client

url = 'http://localhost:8069'
db = 'stadia'
user = 'admin'
passowrd = 'be3327e92d72240272e41918c281f6716a74ce4c'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))

with open('computer_and_acc.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            line_count += 1
    print(f'Processed {line_count} lines.')