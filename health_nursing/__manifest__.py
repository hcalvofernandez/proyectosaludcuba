# Copyright 2011-2020 GNU Solidario <health@gnusolidario.org>
# Copyright 2020 Ing. Yadier Abel de Quesada yadierq87@gmail.com
# Copyright 2020 LabViv
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'GNU Health nursing',
    'summary': 'GNU Health nursing functionality package',
    'version': '0.0.1',
    'category': 'Medical',
    'depends': [
        'medical',
        'medical_extras',
        'health_lifestyle',
        'medical_inpatient',
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
        'data/health_nursing_sequences.xml',
        'views/gnuhealth_ambulatory_care.xml',
        'views/gnuhealth_ambulatory_procedure_tree.xml',
        'views/gnuhealth_patient_ambulatory_care.xml',
        'views/gnuhealth_patient_ambulatory_care_tree.xml',
        'views/gnuhealth_patient_rounding.xml',
        'views/gnuhealth_patient_rounding_tree.xml',
        'views/gnuhealth_procedure_tree.xml',
        'views/gnuhealth_rounding_procedure.xml',
        'views/health_nursing_view.xml',
        'report/round_report.xml',
        'report/health_nursing_report.xml',
        #'security/access_rights.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'installable': True,
    'application': True,
}
