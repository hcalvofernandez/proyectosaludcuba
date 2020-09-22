# -*- coding: utf-8 -*-
{
    'name': 'medical_ntd_chagas',
    'summary': 'GNU Health package for hospitalization calendar functionality',
    'version': '0.0.1',
    'category': 'Medical',
    'depends': [
        'medical_ntd',
    ],
    'Author': 'GNU Solidario',
    'email': 'health@gnusolidario.org',
    'website': "https://www.gnuhealth.org",
    'description': """
                GNU Health Neglected Tropical Diseases. Chagas package.
    """,
    'license': 'GPL-3',
    'data': [
          'security/security.xml',
          'security/ir.model.access.csv',
          'data/medical_ntd_chagas_sequence.xml',
          'views/medical_ntd_chagas_view.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
}
