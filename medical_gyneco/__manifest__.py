# -*- coding: utf-8 -*-
# Copyright Copyright 2020 NeoHan Solutions Cuba
#    para GNU Solidario  <health@gnusolidario.org>
# Copyright (C) 2011-2020 Luis Falcon <falcon@gnuhealth.org>
# Copyright (C) 2011-2020 GNU Solidario <health@gnusolidario.org>
# Copyright (C) 2011 Cédric Krier

{
    'name': "Medical Gynecology",
    'summary': """
        GNU Health Gynecology and Obstetrics package
    """,
    'description': """
        Medical Gyneco Module
        ##########################

        This module includes:

            * Gynecological Information
            * Obstetric information
            * Perinatal Information and monitoring
            * Puerperium
    """,
    'author': "GNU Solidario",
    'website': "https://www.gnuhealth.org",
    'category': 'Medical',
    'version': '13.0.1',
    'depends': ['base', 'medical'],
    'data': [
        'security/ir.model.access.csv',
        'views/medical_gyneco_view.xml',
        # data/gnuhealth_commands.xml,
        # security/access_rights.xml,
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'maintainer': 'Yoinier Hernandez Nieves <yoinier.hn@gmail.com>'
}
