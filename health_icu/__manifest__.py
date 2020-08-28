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
	'author_name': "Yadier A. De Quesada",
	'author_email': "yadierq87@gmail.com",
    'website': "https://www.gnuhealth.org",

    'category': 'Healthcare Industry',
    'version': '0.0.1',

    # any module necessary for this one to work correctly
    #TODO depends nursing
    #health_nursing
    'depends': ['base','medical','medical_inpatient','medical_extras'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/gnuhealth_icu_apache2_form.xml',
        'views/gnuhealth_icu_apache2_tree.xml',
        'views/gnuhealth_icu_chest_drainage_form.xml',
        'views/gnuhealth_icu_chest_drainage_tree.xml',
        'views/gnuhealth_icu_glasgow_form.xml',
        'views/gnuhealth_icu_glasgow_tree.xml',
        'views/gnuhealth_icu_ventilation_form.xml',
        'views/gnuhealth_icu_ventilation_tree.xml',
        'views/gnuhealth_inpatient_icu_form.xml',
        'views/gnuhealth_inpatient_icu_tree.xml',
        #'views/gnuhealth_patient_icu_rounding.xml',
        'views/health_icu_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
