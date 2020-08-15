# Copyright 2011-2020 GNU Solidario <health@gnusolidario.org>
# Copyright 2020 LabViv
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'Health Inpatient',
    'summary': 'GNU Health hospitalization management package.',
    'version': '13.0.0.0.1',
    'category': 'Medical',
    'depends': [
        'medical',
        'health_lifestyle',
    ],
    'Author': 'GNU Solidario',
    'website': "https://www.gnuhealth.org",
    'description': """
        - Hospitalización del paciente, asignación de camas, planes de cuidado y enfermería. .
    """,
    'license': 'GPL-3',
    'data': [
        'views/health_inpatient_menu.xml',
        'views/gnuhealth_appointment_form_view_extend.xml',
        'views/gnuhealth_bed_transfer_form_view.xml',
        'views/gnuhealth_inpatient_diet_form_view.xml',
        'views/gnuhealth_inpatient_diet_therapeutic_form_view.xml',
        'views/gnuhealth_inpatient_meal_form_view.xml',
        'views/gnuhealth_inpatient_meal_order_form_view.xml',
        'views/gnuhealth_inpatient_meal_order_item_form_view.xml',
        'views/gnuhealth_inpatient_med_admin_time_form_view.xml',
        'views/gnuhealth_inpatient_med_log_form_view.xml',
        'views/gnuhealth_inpatient_medication_form_view.xml',
        'views/gnuhealth_inpatient_registration_view.xml',
        'views/gnuhealth_patient_ecg_form_view_extend.xml',
        'views/gnuhealth_patient_evaluation_form_view_extend.xml',
        'views/gnuhealth_patient_form_view_extend.xml',
        'views/gnuhealth_patient_tree_view_extend.xml',
        'data/health_inpatient_sequence.xml',
        'data/inpatient_diets.xml',
        'security/access_rights.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'installable': True,
    'application': True,
}
