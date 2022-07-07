import csv
import xmlrpc.client
import pandas as pd
from datetime import datetime

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


# with open('manpower.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     job =  models.execute_kw(db, uid, password, 'hr.department', 'search', [[['name', '=', 'Management']]])
#     employee_id = models.execute_kw(db, uid, password, 'hr.employee', 'create', [{
#             'name': 'Ababe',
#             'gender': 'male',
#             'job_id': job[0],
#             # 'department_id': (1, False, 1)
#         }])
#     # job_id = models.execute_kw(db, uid, password, 'hr.employee', 'write', [{
#     #         'job_id': 
#     #     }])
#     print(job)
#     print(employee_id)

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

df = pd.read_excel('manpower.xlsx')

for index, row in df.iterrows():
    print(row['Name of Employee'])
    job =  models.execute_kw(db, uid, password, 'hr.job', 'search', [[['name', '=', row['Position'].strip()]]])
    department =  models.execute_kw(db, uid, password, 'hr.department', 'search', [[['name', '=', row['Department'].strip()]]])
    salary_structure = models.execute_kw(db, uid, password, 'hr.payroll.structure', 'search', [[['name', '=', 'Base for new structures']]])
    work_place = models.execute_kw(db, uid, password, 'stadia.workplace', 'search', [[['name', '=', row['Project'].strip()]]])
    education = models.execute_kw(db, uid, password, 'hr.field.study', 'search', [[['name', '=', row['Education'].strip()]]])

    if(not education):
        if(row['Education'].strip()):
            education =  models.execute_kw(db, uid, password, 'hr.field.study', 'create', [{'name':row['Education'].strip()}])
        else:
            education = None

    if(not work_place):
        work_place = models.execute_kw(db, uid, password, 'hr.department', 'create', [{'name': row['Project'].strip()}])

    if(not job):
        job[0] = models.execute_kw(db, uid, password, 'hr.job', 'create', [{'name': row['Position'].strip(), 'department_id': department[0]}])

    print(department)
    print(job)

    employee = models.execute_kw(db, uid, password, 'hr.employee', 'create', [{
        'name': row['Name of Employee'].strip(),
        'gender': row['Gender'].strip().lower(),
        'job_id': job[0],
        'department_id': department[0],
        'degree_id': education[0],
        'mobile_phone': str(row['Employee Phone number']).strip()
    }])

    # employee_contract = models.execute_kw(db, uid, password, 'hr.employee', 'create', [{
    #     'name': '%s Contract Agreement' % row['Name of Employee'].strip(),
    #     'gender': employee[0],
    #     'job_id': job[0],
    #     'department_id': department[0],
    #     'struct_id': salary_structure[0],
    #     'work_place_id': work_place[0],
    #     'date_start': datetime.strptime(row['Date of Employment'].strip(), '%m-%d-%Y').date(),
    #     'wage': float(row['Basic salary'].strip()),
    #     'transport_allowance': float(row['Transport Allowance'].strip()),
    #     'perdime': float(row['Perdiem'].strip()),
    # }])