# -*- coding: utf-8 -*-
#    Copyright (C) 2011-2020 Luis Falcon <falcon@gnuhealth.org>
#    Copyright (C) 2011 Cédric Krier

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

{
    'name': 'medical_inpatient_calendar',
    'summary': 'GNU Health package for hospitalization calendar functionality',
    'version': '0.0.1',
    'category': 'Medical',
    'depends': [
        'medical_extras',
        'medical_inpatient',
        'calendar',
        #'health_calendar', TODO incluir
    ],
    'Author': 'GNU Solidario',
    'email': 'health@gnusolidario.org',
    'website': "https://www.gnuhealth.org",
    'description': """
                - GNU Health combines the daily medical practice with state-of-the-art 
        technology in bioinformatics and genetics. It provides a holistic approach 
        to the  person, from the biological and molecular basis of disease to 
        the social and environmental determinants of health.
        
        GNU Health also manages the internal processes of a health institution, 
        such as calendars, financial management, billing, stock management, 
        pharmacies or laboratories (LIMS)
        
        The **GNU Health Federation** allows to interconnect heterogeneous nodes
        and build large federated health networks across a region, province
        or country.
    """,
    'license': 'GPL-3',
    'data': [
        'views/health_inpatient_calendar_view.xml',
        #'security/ir.model.access.csv',
    ],
    'demo': [],
    'installable': True,
    'application': True,
}
