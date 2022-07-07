import csv
import xmlrpc.client

url = 'http://localhost:8069'
db = 'stadia'
user = 'admin'
password = 'be3327e92d72240272e41918c281f6716a74ce4c'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, user, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name': "New Partner"}])

########################################
# Refs and data cleaning
# Departments


with open('manpower.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if(line_count == 0):
            continue

        employee_id = models.execute_kw(db, uid, password, 'hr.employee', 'create', [{
            'name': row[1].strip(),
            'gender': row[2].strip(),
            'job_id': 1
        }])
        print(employee_id)
        break
        line_count += 1