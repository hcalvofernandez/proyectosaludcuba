# -*- coding: utf-8 -*-
{
    'name' : 'GNU Health ophthalmology package',
    'summary': '',
    'description': """GNU Health ophthalmology package
    """,
    'version': '1.0.1',
    'category': 'Hospital Management System',
    'author': 'SoftwareEscarlata',
    'support': 'health@gnusolidario.org',
    'website': 'https://www.gnuhealth.org',
    'license': 'OPL-1',
    'depends' : [
        'base','medical','report_py3o'
    ],
    'data': [
        'views/oph_tree.xml',
        'views/oph_form.xml',
        'views/findings_form.xml',
        'views/findings_tree.xml',
        'views/menu.xml',
        'views/health_ophthalmology_report.xml',
        'security/ir.model.access.csv',

    ],

    'application': False,
    'sequence': 2,
    'currency': 'EUR',
}
