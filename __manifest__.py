{
    'name': 'Chargily Payment Gateway',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Integrate Chargily payment gateway with Odoo e-commerce',
    'description': """
        This module integrates the Chargily payment gateway with Odoo's e-commerce payment methods.
    """,
    'author': 'Your Name',
    'website': 'https://www.example.com',
    'depends': ['website_sale'],
    'data': [
        'views/payment_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
