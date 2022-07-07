import csv
import xmlrpc.client

url = 'http://localhost:8069'
db = 'stadia'
user = 'admin'
password = '354c68c9432e839044c3206e0a2412814329175e'

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
    job =  models.execute_kw(db, uid, password, 'hr.department', 'search', [[['name', '=', 'Management']]])
    employee_id = models.execute_kw(db, uid, password, 'hr.employee', 'create', [{
            'name': 'Ababe',
            'gender': 'male',
            'job_id': job[0],
            # 'department_id': (1, False, 1)
        }])
    # job_id = models.execute_kw(db, uid, password, 'hr.employee', 'write', [{
    #         'job_id': 
    #     }])
    print(job)
    print(employee_id)

    # for row in csv_reader:
    #     if(line_count == 0):
    #         continue
        
    #     if(line_count > 1):
    #         break
        
    #     print('1111111111111111111')

    #     employee_id = models.execute_kw(db, uid, password, 'hr.employee', 'create', [{
    #         'name': row[1].strip(),
    #         'gender': row[2].strip(),
    #         'job_id': 1
    #     }])
    #     print(employee_id)
    #     line_count += 1