# -*- coding: utf-8 -*-
{
    'name': "gnuhealth_icu",

    'summary': """
        GNU Health package for Intensive Care  settings""",

    'description': """
        #. **Hospital Management Information System (HMIS)**
        #. **Electronic Medical Record (EMR)**
        #. **Health Information System (HIS)**
        #. **Laboratory Information System (LIS)**
    """,

    'author': "GNU Solidario",
    'website': "https://www.gnuhealth.org",

    'category': 'Healthcare Industry',
    'version': '0.0.1',

    # any module necessary for this one to work correctly
    #TODO depends 'health'
    #health_inpatient
    #health_nursing
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
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
