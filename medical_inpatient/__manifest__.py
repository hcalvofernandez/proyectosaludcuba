# Copyright 2011-2020 GNU Solidario <health@gnusolidario.org>
# Copyright 2020 LabViv
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'Medical Inpatient',
    'summary': 'Medical hospitalization management package.',
    'version': '13.0.0.0.1',
    'category': 'Medical',
    'depends': [
        'medical',
        'medical_extras',
        'health_lifestyle',
    ],
    'Author': 'GNU Solidario',
    'website': "https://www.gnuhealth.org",
    'description': """
        - Hospitalización del paciente, asignación de camas, planes de cuidado y enfermería. .
    """,
    'license': 'GPL-3',
    'data': [
        'views/medical_inpatient_menu.xml',
        'views/medical_appointment_form_view_extend.xml',
        'views/medical_bed_transfer_view.xml',
        'views/medical_inpatient_diet_view.xml',
        'views/medical_inpatient_diet_therapeutic_view.xml',
        'views/medical_inpatient_meal_view.xml',
        'views/medical_inpatient_meal_order_view.xml',
        'views/medical_inpatient_meal_order_item_view.xml',
        'views/medical_inpatient_med_admin_time_view.xml',
        'views/medical_inpatient_med_log_view.xml',
        'views/medical_inpatient_medication_view.xml',
        'views/medical_inpatient_registration_view.xml',
        'views/medical_patient_ecg_form_view_extend.xml',
        'views/medical_patient_evaluation_form_view_extend.xml',
        'views/medical_patient_form_view_extend.xml',
        'views/medical_patient_tree_view_extend.xml',
        'wizard/medical_bed_transfer_create_wizard_view.xml',
        'wizard/medical_inpatient_evaluation_create_wizard_view.xml',
        'data/medical_inpatient_sequence.xml',
        'data/inpatient_diets.xml',
        'security/access_rights.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'installable': True,
    'application': True,
}
