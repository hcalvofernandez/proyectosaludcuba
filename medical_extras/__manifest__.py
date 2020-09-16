# -*- coding: utf-8 -*-
{
    'name': 'Odoo Medical Extras',
    'summary': 'Extends medical_abstract_entity.',
    'description': 'Medical module ported from OCA/medical-vertical',
    'version': '13.0.0.0.1',
    'category': 'Medical',
    'depends': [
        'product',
        'base_locale_uom_default',
        'medical'
    ],
    'author': "GNU Solidario",
    'website': "https://www.gnuhealth.org",
    'license': 'GPL-3',
    'data': [
        'security/ir.model.access.csv',
        # 'views/template.xml',
        'views/views.xml',
        'views/evaluation.xml',
        'data/medical_extras_sequence.xml',
    ],
    'demo': [
        # 'demo/medical_patient_demo.xml',
    ],
    'installable': True,
    'application': False,
    'maintainer': 'Yoinier Hernandez Nieves <yoinier.hn@gmail.com>'
}
