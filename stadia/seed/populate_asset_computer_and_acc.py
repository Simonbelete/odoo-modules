import csv
import xmlrpc.client
import pandas as pd

url = 'http://localhost:8069'
db = 'stadia'
user = 'admin'
passowrd = 'be3327e92d72240272e41918c281f6716a74ce4c'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, user, passowrd, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

df = pd.read_excel('computer_and_acc.xlsx')

for index, row in df.iterrows():
    print(row['Description'])

    description = str(row['Description']).strip()
    ref_no = str(row['Reference no']).strip()
    partner_name = str(row['Supplier Name']).strip()
    cpv = str(row['Accounts Ref']).strip()
    location_name = str(row['Location']).strip()
    employee_name = str(row['Name']).strip()
    sta_no = str(row['ID.T.No.']).strip()
    ifrs_rate = float(row['ifrs_rate'])
    gross_value = float(row['Cost'])

    # Create or search supplier name in res.partner
    partner_id = 1

    asset =  models.execute_kw(db, uid, passowrd, 'hr.employee', 'create', [{
        'name': description,
        'category_id': 1
    }])