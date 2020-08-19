# Copyright 2011-2020 GNU Solidario <health@gnusolidario.org>
# Copyright 2020 LabViv
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

{
    'name': 'Health Genetics',
    'summary': 'GNU Health Genetics Module.',
    'version': '13.0.0.0.1',
    'category': 'Medical',
    'depends': [
        'medical',
    ],
    'Author': 'GNU Solidario',
    'website': "https://www.gnuhealth.org",
    'description': """
        Riesgos hereditarios. Alrededor de 4200 “disease genes” del NCBI / GeneCards. . .
    """,
    'license': 'GPL-3',
    'data': [
        'views/health_genetics_menu.xml',
        'views/gnuhealth_disease_gene_view.xml',
        'views/gnuhealth_gene_variant_phenotype_view.xml',
        'views/gnuhealth_gene_variant_view.xml',
        'views/gnuhealth_patient_family_diseases_view.xml',
        'views/gnuhealth_patient_form_view_extend.xml',
        'views/gnuhealth_patient_genetic_risk_view.xml',
        'views/gnuhealth_protein_disease_view.xml',
        'data/disease_genes.xml',
        'data/gnuhealth_commands.xml',
        'security/access_rights.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'installable': True,
    'application': True,
}
