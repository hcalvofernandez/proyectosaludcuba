# -*- coding: utf-8 -*-
{
    'name': 'Tropical Diseases. Dengue',
    'summary': 'GNU Health Neglected Tropical Diseases. Dengue package',
    'version': '0.0.1',
    'category': 'Medical',
    'depends': [
        'medical_ntd',
    ],
    'Author': 'GNU Solidario',
    'email': 'health@gnusolidario.org',
    'website': "https://www.gnuhealth.org",
    'description': """
                GNU Health Neglected Tropical Diseases. Dengue package.
    """,
    'license': 'GPL-3',
    'data': [
            'security/security.xml',
            'security/ir.model.access.csv',
            'data/medical_ntd_dengue_sequence.xml',
            'views/medical_ntd_dengue_view.xml'
    ],
    'demo': [],
    'installable': True,
    'application': False,
}
