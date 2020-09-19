# -*- coding: utf-8 -*-
{
    'name': "Medical History",
    'summary': """
        Medical Laboratory Module""",

    'description': """
        GNU Health personal and medical history package
    """,

    'author': "GNU Solidario",
    'website': "https://www.gnuhealth.org",
    'category': 'Uncategorized',
    'version': '0.0.1',
    'depends': [
                'medical_extras',
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
