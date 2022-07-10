import csv
import xmlrpc.client
from numpy import NaN
import pandas as pd
from datetime import datetime, date
from db_conf import url, db, user, password

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, user, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

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

    start_date = row['Date of Employment'].strftime('%Y-%m-%d') if isinstance(row['Date of Employment'], date) else date(1999, 1, 1).strftime('%Y-%m-%d')


    employee_contract = models.execute_kw(db, uid, password, 'hr.contract', 'create', [{
        'employee_id': employee,
        'name': '%s Contract Agreement' % row['Name of Employee'].strip(),
        'job_id': job,
        'department_id': department[0],
        'struct_id': salary_structure[0],
        'work_place_id': work_place,
        'date_start': start_date, #datetime.strptime(row['Date of Employment'], '%Y-%m-%d').strftime('%Y-%m-%d') if isinstance(row['Date of Employment'], str) else row['Date of Employment'].strftime('%Y-%m-%d'),
        'wage': float(row['Basic salary']),
        'transport_allowance': float(row['Transport Allowance']),
        'perdime': float(row['Perdiem']) if row['Perdiem'] else 0,
        'state': 'open'
    }])