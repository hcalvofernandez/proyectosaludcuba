# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'SMS for Medical',
    'version': '1.0',
    'category': 'SMS/MEdical',
    'summary': 'Add SMS capabilities to Medical',
    'description': "",
    'depends': ['calendar'],
    'data': [
        'views/sms_medical_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
