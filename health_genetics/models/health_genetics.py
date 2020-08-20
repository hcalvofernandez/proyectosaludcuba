# -*- coding: utf-8 -*-
##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2020 Luis Falcon <lfalcon@gnusolidario.org>
#    Copyright (C) 2011-2020 GNU Solidario <health@gnusolidario.org>
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
# from datetime import datetime
from odoo import api, fields, models, _
from odoo.osv import expression
from uuid import uuid4

__all__ = ['DiseaseGene', 'ProteinDisease', 'GeneVariant', 'GeneVariantPhenotype',
           'PatientGeneticRisk', 'FamilyDiseases', 'PatientData']


class DiseaseGene(models.Model):
    _description = 'Disease Genes'
    _name = 'gnuhealth.disease.gene'

    name = fields.Char('Gene Name',
                       required=True,
                       index=True)
    protein_name = fields.Char('Protein Code',
                               help="Encoding Protein Code, such as UniProt protein name",
                               index=True)
    long_name = fields.Char('Official Long Name',
                            translate=True)
    gene_id = fields.Char('Gene ID',
                          help="default code from NCBI Entrez database.",
                          index=True)
    chromosome = fields.Char('Chromosome',
                             help="Name of the affected chromosome",
                             index=True)
    location = fields.Char('Location',
                           help="Locus of the chromosome")

    info = fields.Text('Information',
                       help="Extra Information")
    variants = fields.One2many('gnuhealth.gene.variant',
                               'name',
                               'Variants')

    protein_uri = fields.Char('Protein URI',
                              compute='_get_protein_uri')

    @api.depends('name', 'protein_name')
    def _get_protein_uri(self):
        for record in self:
            if record.protein_name:
                record.protein_uri = 'http://www.uniprot.org/uniprot/' + str(record.protein_name)

    _sql_constraints = [
        ('name_unique', 'unique (name)', 'The Official Symbol name must be unique!'),
    ]

    def _get_name(self):
        # self.ensure_one()
        protein = ''
        if self.protein_name:
            protein = ' (' + self.protein_name + ') '
        return self.name + protein + ':' + self.long_name

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if operator.startswith('!') or operator.startswith('not '):
            domain = [('name', operator, name),
                      ('long_name', operator, name)]
        else:
            domain = ['|',
                      ('name', operator, name),
                      ('long_name', operator, name)]
        rec = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(rec).with_user(name_get_uid))


class ProteinDisease(models.Model):
    _description = 'Protein related disorders'
    _name = 'gnuhealth.protein.disease'

    name = fields.Char('Disease',
                       required=True,
                       index=True,
                       help="Uniprot Disease Code")

    disease_name = fields.Char('Disease name',
                               translate=True)
    acronym = fields.Char('Acronym',
                          required=True,
                          index=True,
                          help="Disease acronym / mnemonics")
    disease_uri = fields.Char('Disease URI',
                              compute='_get_disease_uri')

    mim_reference = fields.Char('MIM',
                                help="MIM -Mendelian Inheritance in Man- DB reference")

    gene_variant = fields.One2many('gnuhealth.gene.variant.phenotype',
                                   'phenotype',
                                   'Natural Variant',
                                   help="Protein sequence variant(s) involved in this condition")

    dominance = fields.Selection([(None, ''),
                                  ('d', 'dominant'),
                                  ('r', 'recessive'),
                                  ('c', 'codominance'), ],
                                 'Dominance',
                                 index=True)

    description = fields.Text('Description')

    @api.depends('name')
    def _get_disease_uri(self):
        self.ensure_one()
        ret_url = ''
        if self.name:
            ret_url = 'http://www.uniprot.org/diseases/' + str(self.name)
        return ret_url

    _sql_constraints = [
        ('name_unique', 'unique (name)', 'The Disease Code  name must be unique!'),
    ]

    def _get_name(self):
        # self.ensure_one()
        return self.name + ':' + self.disease_name

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if operator.startswith('!') or operator.startswith('not '):
            domain = [('name', operator, name),
                      ('disease_name', operator, name)]
        else:
            domain = ['|',
                      ('name', operator, name),
                      ('disease_name', operator, name)]
        rec = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(rec).with_user(name_get_uid))


class GeneVariant(models.Model):
    _description = 'Natural Variant'
    _name = 'gnuhealth.gene.variant'

    name = fields.Many2one('gnuhealth.disease.gene',
                           'Gene and Protein',
                           required=True,
                           help="Gene and expressing protein (in parenthesis)")
    variant = fields.Char("Protein Variant",
                          required=True,
                          index=True)
    aa_change = fields.Char('Change',
                            help="Resulting amino acid change")
    phenotypes = fields.One2many('gnuhealth.gene.variant.phenotype',
                                 'variant',
                                 'Phenotypes')

    _sql_constraints = [
        ('variant_unique', 'unique (variant)', 'The variant ID must be unique!'),
        ('aa_unique', 'unique (variant, aa_change)', 'The resulting AA change for this protein already exists!'),
    ]

    def _get_name(self):
        # self.ensure_one()
        return ' : '.join([self.variant, self.aa_change])

    # Allow to search by gene and variant or amino acid change
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if operator.startswith('!') or operator.startswith('not '):
            domain = [('name', operator, name),
                      ('variant', operator, name),
                      ('aa_change', operator, name)]
        else:
            domain = ['|', '|',
                      ('name', operator, name),
                      ('variant', operator, name),
                      ('aa_change', operator, name)]
        rec = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(rec).with_user(name_get_uid))


class GeneVariantPhenotype(models.Model):
    _description = 'Variant Phenotypes'
    _name = 'gnuhealth.gene.variant.phenotype'

    name = fields.Char('Code',
                       required=True)
    variant = fields.Many2one('gnuhealth.gene.variant',
                              'Variant',
                              required=True)
    gene = fields.Many2one('gnuhealth.disease.gene',
                           'Gene & Protein',
                           compute='_get_gene',
                           search='_search_gene',
                           help="Gene and expressing protein (in parenthesis)")
    phenotype = fields.Many2one('gnuhealth.protein.disease',
                                'Phenotype',
                                required=True)

    @api.depends('variant')
    def _get_gene(self):
        if self.variant:
            return self.variant.name.id

    def _get_name(self):
        if self.phenotype:
            return self.phenotype.name

    def _search_gene(self, operator, value):
        res = []
        res.append(('variant.name', operator, value))
        return res

    # Allow to search by gene, variant or phenotype
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if operator.startswith('!') or operator.startswith('not '):
            domain = [('name', operator, name),
                      ('variant.name', operator, name),
                      ('phenotype.name', operator, name),
                      ('gene.name', operator, name)]
        else:
            domain = ['|', '|', '|',
                      ('name', operator, name),
                      ('variant.name', operator, name),
                      ('phenotype.name', operator, name),
                      ('gene.name', operator, name)]
        rec = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(rec).with_user(name_get_uid))

    _sql_constraints = [
        ('code_uniq', 'unique (name)', 'This code already exists!'),
    ]


class PatientGeneticRisk(models.Model):
    _description = 'Patient Genetic Information'
    _name = 'gnuhealth.patient.genetic.risk'

    patient = fields.Many2one('medical.patient',
                              'Patient',
                              index=True)
    disease_gene = fields.Many2one('gnuhealth.disease.gene',
                                   'Gene',
                                   required=True)
    natural_variant = fields.Many2one('gnuhealth.gene.variant',
                                      'Variant',
                                      depends=['disease_gene'])
    variant_phenotype = fields.Many2one('gnuhealth.gene.variant.phenotype',
                                        'Phenotype',
                                        depends=['natural_variant'])
    onset = fields.Integer('Onset',
                           help="Age in years")

    notes = fields.Char("Notes")

    healthprof = fields.Many2one('gnuhealth.healthprofessional',
                                 'Health prof',
                                 help="Health professional")

    institution = fields.Many2one('gnuhealth.institution',
                                  'Institution')

    def default_institution(self):
        HealthInst = self.env['gnuhealth.institution']
        institution = HealthInst.get_institution()
        return institution

    def create_genetics_pol(self, genetic_info):
        """ Adds an entry in the person Page of Life
            related to this genetic finding
        """
        Pol = self.env['gnuhealth.pol']
        pol = []

        vals = {
            'page': str(uuid4()),
            'person': genetic_info.patient.name.id,
            'age': genetic_info.onset and str(genetic_info.onset) + 'y' or '',
            'federation_account': genetic_info.patient.name.federation_account,
            'page_type': 'medical',
            'medical_context': 'genetics',
            'relevance': 'important',
            'gene': genetic_info.disease_gene.rec_name,
            'natural_variant': genetic_info.natural_variant and genetic_info.natural_variant.aa_change,
            'summary': genetic_info.notes,
            'author': genetic_info.healthprof and genetic_info.healthprof.name.rec_name,
            'node': genetic_info.institution and genetic_info.institution.name.rec_name
        }
        if genetic_info.variant_phenotype:
            vals['health_condition_text'] = vals['health_condition_text'] = \
                genetic_info.variant_phenotype.phenotype.rec_name

        pol.append(vals)
        Pol.create(pol)

    @api.model_create_multi
    def create(self, vals_list):

        # Execute first the creation of PoL
        genetic_info = super(PatientGeneticRisk, self).create(vals_list)

        self.create_genetics_pol(genetic_info[0])

        return genetic_info

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if operator.startswith('!') or operator.startswith('not '):
            domain = [('name', operator, name),
                      ('patient.name', operator, name),
                      ('disease_gene.name', operator, name),
                      ('variant_phenotype.name', operator, name)]
        else:
            domain = ['|', '|', '|',
                      ('name', operator, name),
                      ('patient.name', operator, name),
                      ('disease_gene.name', operator, name),
                      ('variant_phenotype.name', operator, name)]
        rec = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(rec).with_user(name_get_uid))


class FamilyDiseases(models.Model):
    _description = 'Family History'
    _name = 'gnuhealth.patient.family.diseases'

    patient = fields.Many2one('medical.patient',
                              'Patient',
                              index=True)
    name = fields.Many2one('gnuhealth.pathology',
                           'Condition',
                           required=True)
    xory = fields.Selection([(None, ''),
                             ('m', 'Maternal'),
                             ('f', 'Paternal'),
                             ('s', 'Sibling'), ],
                            'Maternal or Paternal',
                            index=True)

    relative = fields.Selection([('mother', 'Mother'),
                                 ('father', 'Father'),
                                 ('brother', 'Brother'),
                                 ('sister', 'Sister'),
                                 ('aunt', 'Aunt'),
                                 ('uncle', 'Uncle'),
                                 ('nephew', 'Nephew'),
                                 ('niece', 'Niece'),
                                 ('grandfather', 'Grandfather'),
                                 ('grandmother', 'Grandmother'),
                                 ('cousin', 'Cousin'), ],
                                'Relative',
                                help='First degree = siblings, mother and father\n'
                                     'Second degree = Uncles, nephews and Nieces\n'
                                     'Third degree = Grandparents and cousins',
                                required=True)


class MedicalPatient(models.Model):
    """Add to the Medical patient_data class (gnuhealth.patient) the genetic and family risks"""
    _name = 'medical.patient'
    _inherit = 'medical.patient'

    genetic_risks = fields.One2many('gnuhealth.patient.genetic.risk',
                                    'patient',
                                    'Genetic Information')
    family_history = fields.One2many('gnuhealth.patient.family.diseases',
                                     'patient',
                                     'Family History')
