import csv
import xmlrpc.client
import pandas as pd
from datetime import datetime, date
from db_conf import url, db, user, password

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, user, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

df = pd.read_excel('vehicles.xlsx')

for index, row in df.iterrows():
    print(row['Description'])

    category_id = models.execute_kw(db, uid, password, 'stadia.asset.category', 'search', [[['name', '=', 'Furniture and Equipment']]])
    category_id = category_id[0]
    description = str(row['Description']).strip()
    ref_no = str(row['Reference no']).strip()
    partner_name = str(row['Supplier Name']).strip()
    cpv = str(row['Accounts Ref']).strip()
    # location_name = str(row['Location']).strip()
    employee_name = str(row['Name']).strip()
    sta_no = str(row['ID.T.No.']).strip()
    ifrs_rate = float(row['ifrs_rate'])
    gross_value = float(row['Cost'])
    purchase_date = row['Date of Purchase'].strftime('%Y-%m-%d')

    print(sta_no)
    print(row['Date of Purchase'])

    # Create or search supplier name in res.partner
    partner_id = models.execute_kw(db, uid, password, 'stadia.asset.category', 'search', [[['name', '=', partner_name]]])
    if(len(partner_id) == 0):
        # Create new Partner
        partner_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
            'name': partner_name,
        }])
    else:
        partner_id = partner_id[0]

    asset = models.execute_kw(db, uid, password, 'stadia.asset', 'create', [{
        'name': description,
        'purchase_date': purchase_date,
        'category_id': category_id,
        'partner_id': partner_id,
        'reference_no': ref_no,
        'id_t_no': sta_no,
        'ifrs_rate': ifrs_rate,
        'gross_value': gross_value,
        'cpv': cpv
    }])

    amount = float(row['Deperciation Amount'])
    acc_amount = float(row['ACC. Depreciation   /IFRS'])
    remaining_value = float(row['NBV/IFRS'])

    asset_depreciation = models.execute_kw(db, uid, password, 'stadia.asset.depreciation.line', 'create', [{
        'sequence': 1,
        'asset_id': asset,
        'amount': amount,
        'depreciated_value': acc_amount,
        'depreciation_date': date(2021, 9, 11).strftime('%Y-%m-%d'),
        'remaining_value': remaining_value
    }])

    # employee_id = None
    # location_id = None

    # if(len(location_name) < 1 and len(employee_name) < 1):
    #     continue

    # if(len(location_name) > 0 and location_name == 'STORE'):
    #     location_id = models.execute_kw(db, uid, password, 'asset.location', 'search', [[['name', '=', location_name]]])
    #     location_id = location_id[0]
    # elif (len(location_name) > 0):
    #     location_id = models.execute_kw(db, uid, password, 'asset.location', 'search', [[['name', '=', location_name]]])
    #     if(len(location_id) == 0):
    #         location_id = models.execute_kw(db, uid, password, 'asset.location', 'create', [{
    #             'name': location_name,
    #         }])
    #     else:
    #         location_id = location_id[0]
        
    #     employee_id = models.execute_kw(db, uid, password, 'hr.employee', 'search', [[['name', '=', employee_name]]])
    #     employee_id = employee_id[0]

    print('---------------------------------')