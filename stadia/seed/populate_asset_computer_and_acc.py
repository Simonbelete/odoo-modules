import csv
import xmlrpc.client
import pandas as pd

url = 'http://localhost:8069'
db = 'rd-demo'
user = 'admin'
password = 'cc8f5a3c2ceecb9b0ce65f4e71aee6cfc07a8105'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, user, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

df = pd.read_excel('computer_and_acc.xlsx')

for index, row in df.iterrows():
    print(row['Description'])

    category_id = models.execute_kw(db, uid, password, 'stadia.asset.category', 'search', [[['name', '=', 'Computer and Related Accessories']]])
    category_id = category_id[0]
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
    partner_id = models.execute_kw(db, uid, password, 'stadia.asset.category', 'search', [[['name', '=', partner_name]]])
    if(len(partner_id) == 0):
        # Create new Partner
        partner_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
            'name': partner_name,
        }])
    else:
        partner_id = partner_id[0]

    location_id = models.execute_kw(db, uid, password, 'asset.location', 'search', [[['name', '=', location_name]]])
    if(len(location_id) == 0):
        location_id = models.execute_kw(db, uid, password, 'asset.location', 'create', [{
            'name': location_name,
        }])
    else:
        location_id = location_id[0]

    employee_id = models.execute_kw(db, uid, password, 'hr.employee', 'search', [[['name', '=', employee_name]]])
    if(len(employee_id) == 0):
        print('%s Employee Not Found' % employee_name)
        break
    else:
        employee_id = employee_id[0]

    asset = models.execute_kw(db, uid, password, 'hr.employee', 'create', [{
        'name': description,
        'category_id': category_id,
        'partner_id': partner_id,
        'reference_no': ref_no,
        'location': 'location_id',
        'employee_id': employee_id,
        'id_t_no': sta_no,
        'ifrs_rate': ifrs_rate,
        'gross_value': gross_value
    }])