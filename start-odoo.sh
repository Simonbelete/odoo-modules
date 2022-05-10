#!/bin/sh

./odoo/odoo-bin -c ./odoo/odoo.conf

./odoo/odoo-bin -c ./odoo/odoo.conf  --addons-path=./modules
./odoo/odoo-bin -c ./odoo/odoo.conf  --addons-path=./modules,./odoo/addons

./odoo/odoo-bin -c ./odoo/odoo.conf --addons-path=./modules,./odoo/addons -d rd-demo
# Update/ Reload
./odoo/odoo-bin -c ./odoo/odoo.conf --addons-path=./modules,./odoo/addons -d rd-demo -u estate

In order to avoid relaunching the server every time you do a modification to the view, it can be convenient to use the --dev xml parameter when launching the server:

./odoo/odoo-bin -c ./odoo/odoo.conf --addons-path=./modules,./odoo/addons -d rd-demo -u estate --dev xml