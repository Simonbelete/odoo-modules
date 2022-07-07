import csv
import xmlrpc.client

url = 'http://localhost:8069'
db = 'stadia'
user = 'admin'
password = 'be3327e92d72240272e41918c281f6716a74ce4c'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, user, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name': "New Partner"}])

print(id)