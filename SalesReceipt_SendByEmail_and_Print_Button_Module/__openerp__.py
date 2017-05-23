#######################################################################

{
    'name': 'Sales Receipt Send By Email and Print Button Module',
    'version': '1.0',
    'website': 'www.hashmicro.com',
    'author': ' Hashmicro / Bharat Chauhan',
    'website': 'www.hashmicro.com',
    'depends': ['account', 'account_voucher', 'mail', 'base', 'bee_choo_custom_fields'],
    'data': [
        'views/sales_receipt.xml',
        'views/report_sales_receipt.xml',
        'data/sales_receipt_data.xml',
        'views/account_voucher.xml',
        'views/report_layout.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: