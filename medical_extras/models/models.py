# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.osv import expression


class MedicalPatientExtends(models.Model):
    _inherit = 'medical.patient'
    _description = 'Medical Patient Extends'

    blood_type = fields.Selection(
        [
            ('A', 'A'),
            ('B', 'B'),
            ('AB', 'AB'),
            ('O', 'O'),
        ],
        string='Blood Type',
        sort=False
    )

    rh = fields.Selection(
        [
            ('+', '+'),
            ('-', '-'),
        ],
        string='Rh'
    )

    hb = fields.Selection(
        [
            ('aa', 'AA'),
            ('as', 'AS'),
            ('ss', 'SS'),
            ('sc', 'SC'),
            ('cc', 'CC'),
            ('athal', 'A-THAL'),
            ('bthal', 'B-THAL'),
        ],
        string='Hb',
        help="Clinically relevant Hemoglobin types\n"
        "AA = Normal Hemoglobin\n"
        "AS = Sickle Cell Trait\n"
        "SS = Sickle Cell Anemia\n"
        "AC = Sickle Cell Hemoglobin C Disease\n"
        "CC = Hemoglobin C Disease\n"
        "A-THAL = A Thalassemia groups\n"
        "B-THAL = B Thalassemia groups\n"
    )


class MedicalInstitution(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    def get_institution(self):
        # Retrieve the institution associated to this GNU Health instance
        # That is associated to the Company.

        if self.env.company and self.env.company.partner_id.is_institution:
            return self.env.company.partner_id.id
        else:
            return False

    code = fields.Char(
        string='Code',
        help="Institution code"
    )

    picture = fields.Binary(
        string='Picture'
    )

    institution_type = fields.Selection(
        [
            ('none', ''),
            ('doctor_office', 'Doctor office'),
            ('primary_care', 'Primary Care Center'),
            ('clinic', 'Clinic'),
            ('hospital', 'General Hospital'),
            ('specialized', 'Specialized Hospital'),
            ('nursing_home', 'Nursing Home'),
            ('hospice', 'Hospice'),
            ('rural', 'Rural facility'),
        ],
        string='Type',
        sort=False
    )

    beds = fields.Integer(
        string="Beds"
    )

    operating_room = fields.Boolean(
        string="Operating Room",
        help="Check this box if the institution has operating rooms",
    )

    or_number = fields.Integer(
        string="ORs"
    )

    public_level = fields.Selection(
        [
            ('none', ''),
            ('private', 'Private'),
            ('public', 'Public'),
            ('mixed', 'Private - State')
        ],
        string='Public Level',
        sort=False
    )

    teaching = fields.Boolean(
        string="Teaching",
        help="Mark if this is a teaching institution"
    )

    heliport = fields.Boolean(
        string="Heliport"
    )

    is_institution = fields.Boolean(
        string="Is institution"
    )

    trauma_center = fields.Boolean(
        string="Trauma Center"
    )

    trauma_level = fields.Selection(
        [
            ('none', ''),
            ('one', 'Level I'),
            ('two', 'Level II'),
            ('three', 'Level III'),
            ('four', 'Level IV'),
            ('five', 'Level V'),
        ],
        string='Trauma Level',
        sort=False
    )

    extra_info = fields.Text(
        string="Extra Info"
    )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'This Institution already exists!'),
        ('code_uniq', 'unique (code)', 'This CODE already exists!'),
    ]


class MedicalPathology(models.Model):
    _name = 'medical.pathology'
    _description = 'Health Conditions'

    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
        help='Health condition name'
    )

    code = fields.Char(
        string='Code',
        required=True,
        help='Specific Code for the Disease (eg, ICD-10)'
    )
    # category = fields.Many2one('gnuhealth.pathology.category', 'Main Category',
    #                            help='Select the main category for this disease This is usually'
    #                                 ' associated to the standard. For instance, the chapter on the ICD-10'
    #                                 ' will be the main category for de disease')
    #
    # groups = fields.One2many('gnuhealth.disease_group.members', 'name',
    #                          'Groups', help='Specify the groups this pathology belongs. Some'
    #                                         ' automated processes act upon the code of the group')

    chromosome = fields.Char(
        string='Affected Chromosome',
        help='chromosome number'
    )

    protein = fields.Char(
        string='Protein involved',
        help='Name of the protein(s) affected'
    )

    gene = fields.Char(
        string='Gene',
        help='Name of the gene(s) affected'
    )

    info = fields.Text(
        string='Extra Info'
    )

    active = fields.Boolean(
        string='Active',
        index=True,
        default=True
    )

    def _get_name(self):
        if self.name and self.code:
            return self.code + ' : ' + self.name

    # Search by the health condition code or the description
    @classmethod
    def search_rec_name(cls, name, clause):
        if clause[1].startswith('!') or clause[1].startswith('not '):
            bool_op = 'AND'
        else:
            bool_op = 'OR'
        return [bool_op,
                ('code',) + tuple(clause[1:]),
                ('name',) + tuple(clause[1:]),
                ]

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if operator.startswith('!') or operator.startswith('not '):
            domain = [
                ('name', operator, name),
                ('code', operator, name),
            ]
        else:
            domain = ['|',
                      ('name', operator, name),
                      ('code', operator, name),
                      ]
        rec = self._search(expression.AND(
            [domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(rec).with_user(name_get_uid))

    _sql_constraints = [
        ('code_uniq', 'unique (code)', 'The disease code must be unique!'),
    ]
