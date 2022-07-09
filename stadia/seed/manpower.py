import csv
import xmlrpc.client
from numpy import NaN
import pandas as pd
from datetime import datetime
from db_conf import *

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

    job = models.execute_kw(db, uid, password, 'hr.job', 'search', [[['name', '=', str(row['Position']).strip()]]])
    department =  models.execute_kw(db, uid, password, 'hr.department', 'search', [[['name', '=', str(row['Department']).strip()]]])
    salary_structure = models.execute_kw(db, uid, password, 'hr.payroll.structure', 'search', [[['name', '=', 'Base for new structures']]])
    work_place = models.execute_kw(db, uid, password, 'stadia.workplace', 'search', [[['name', '=', str(row['Project']).strip()]]])
    degree = models.execute_kw(db, uid, password, 'hr.degree', 'search', [[['name', '=', str(row['Education']).strip()]]])
    education = models.execute_kw(db, uid, password, 'hr.field.study', 'search', [[['name', '=', str(row['Specialized  in']).strip()]]])

    if(not degree):
        if(str(row['Education']).strip()):
            degree =  models.execute_kw(db, uid, password, 'hr.degree', 'create', [{'name': str(row['Education']).strip() }])
        else:
            degree = None
    else:
        degree = degree[0]

    if(not education):
        education
        if(str(row['Specialized  in']).strip()):
            education =  models.execute_kw(db, uid, password, 'hr.field.study', 'create', [{'name': str(row['Specialized  in']).strip()}])
        else:
            education = None
    else:
        education = education[0]

    if(not work_place):
        work_place = models.execute_kw(db, uid, password, 'stadia.workplace', 'create', [{'name': str(row['Project']).strip()}])
    else:
        work_place = work_place[0]

    print(department)

    if(not job):
        job = models.execute_kw(db, uid, password, 'hr.job', 'create', [{'name': str(row['Position']).strip(), 'department_id': department[0]}])
    else:
        job = job[0]

    employee = models.execute_kw(db, uid, password, 'hr.employee', 'create', [{
        'name': str(row['Name of Employee']).strip(),
        'gender': str(row['Gender']).strip().lower(),
        'job_id': job,
        'department_id': department[0],
        'degree_id': degree,
        'education_id': education,
        'mobile_phone': str(row['Employee Phone number']).strip()
    }])

    print(str(row['Date of Employment']))
    print('-----------------')


    employee_contract = models.execute_kw(db, uid, password, 'hr.contract', 'create', [{
        'name': '%s Contract Agreement' % row['Name of Employee'].strip(),
        'job_id': job,
        'department_id': department[0],
        'struct_id': salary_structure[0],
        'work_place_id': work_place,
        'date_start': row['Date of Employment'].strftime('%Y-%m-%d') if row['Date of Employment'] else '', #datetime.strptime(row['Date of Employment'], '%Y-%m-%d').strftime('%Y-%m-%d') if isinstance(row['Date of Employment'], str) else row['Date of Employment'].strftime('%Y-%m-%d'),
        'wage': float(row['Basic salary']),
        'transport_allowance': float(row['Transport Allowance']),
        'perdime': float(row['Perdiem']) if row['Perdiem'] else 0,
    }])