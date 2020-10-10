# -*- coding: utf-8 -*-
{
    'name': 'Community commed disability',
    'summary': 'Community commed package for patient Functioning and disability,'
               ' including WHO ICF, migrated from GNU Health',
    'version': '13.0.0.0.1',
    'category': 'commed',
    'author': 'LabViv',
    'website': 'https://git.labviv.org.ve/',
    'license': 'GPL-3',
    'description': """Community commed package for patient Functioning and disability, including WHO ICF.""",
    'depends': [
        'base',
        'commed_base',
    ],
    'data': [
          'security/ir.model.access.csv',
          'data/categories.xml',
          'data/activity_and_participation.xml',
          'data/body_functions.xml',
          'data/body_structures.xml',
          'data/environmental_factors.xml',
          'views/views.xml',
          'views/inherit_views.xml',
          'views/menu.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
}

