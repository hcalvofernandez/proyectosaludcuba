# -*- coding: utf-8 -*-
{
    'name': "gnuhealth_imaging",

    'summary': """
        GNU Health Diagnostic Imaging management package""",

    'description': """
        GNU Health Diagnostic Imaging management package
        - Imaging types and tests.
        - Imaging test requests and results.
    """,

    'author': "GNU Solidario",
    'website': "https://www.gnuhealth.org",

    'category': 'Healthcare Industry',
    'version': '0.0.1',

    # any module necessary for this one to work correctly
    #TODO depends 'health'
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/imaging_test_form.xml',
        'views/imaging_test_request_form.xml',
        'views/imaging_test_request_tree.xml',
        'views/imaging_test_result_form.xml',
        'views/imaging_test_tree.xml',
        'views/imaging_test_result_tree.xml',
        'views/imaging_test_type_form.xml',
        'views/imaging_test_type_tree.xml',
        'views/patient_imaging_test_request_start_form.xml',
        #data
        'data/gnuhealth_commands.xml',
        'data/health_imaging_sequences.xml',
        'data/imaging_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
