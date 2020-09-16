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
    'author_name': "Yadier A. De Quesada",
    'author_email':"yadierq87@gmail.com",
    'website': "https://www.gnuhealth.org",

    'category': 'Healthcare Industry',
    'version': '0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','medical'],

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
        #'wizard/wizard_health_imaging_views.xml', TODO a wizard
        'views/health_imaging_view.xml',
        #data
        'data/gnuhealth_commands.xml',
        'data/health_imaging_sequences.xml',
        'data/imaging_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
