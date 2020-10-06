# -*- coding: utf-8 -*-
{
<<<<<<< HEAD
    'name': "Medical History",
    'summary': """
        Medical Laboratory Module""",
=======
    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
>>>>>>> pruebas

    'description': """
        GNU Health personal and medical history package
    """,

    'author': "GNU Solidario",
    'website': "https://www.gnuhealth.org",
    'category': 'Uncategorized',
    'version': '0.0.1',
    'depends': [
                'medical_extras',
<<<<<<< HEAD
=======
                'medical_genetics',
>>>>>>> pruebas
                'medical_gyneco',
                'health_lifestyle',
                'health_vaccination'
                ],
    'data': [
        'reports/report_definition.xml',
        'reports/patient_evaluation_report.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
}
