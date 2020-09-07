# -*- coding: utf-8 -*-
# Copyright Copyright 2020 NeoHan Solutions Cuba
#    para GNU Solidario  <health@gnusolidario.org>
# Copyright (C) 2011-2020 Luis Falcon <falcon@gnuhealth.org>
# Copyright (C) 2011-2020 GNU Solidario <health@gnusolidario.org>
# Copyright (C) 2011 Cédric Krier

{
    'name': "Medical Laboratory",
    'summary': """
        Medical Laboratory Module
    """,
    'description': """
        Medical Laboratory Module
        ##########################

        This modules includes lab tests:

            * Values
            * Reports
            * PoS
    """,
    'author': "GNU Solidario",
    'website': "https://www.gnuhealth.org",
    'category': 'Medical',
    'version': '13.0.2',
    'depends': ['base', 'medical', 'medical_disease'],
    'data': [
        'security/ir.model.access.csv',
        'views/medical_lab_view.xml',
        # 'health_lab_report.xml',
        'data/medical_lab_sequences.xml',
        # 'data/lab_test_data.xml',
        # 'data/gnuhealth_commands.xml',
        # 'wizard/create_lab_test.xml',
        # 'security/access_rights.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'maintainer': 'Yoinier Hernandez Nieves <yoinier.hn@gmail.com>'
}
