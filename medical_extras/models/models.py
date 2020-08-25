# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.osv import expression
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError


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


# PATIENT APPOINTMENT
class Appointment(models.Model):
    _name = 'medical.appointment'
    _description = 'Patient Appointments'
    _order = "appointment_date desc"

    @api.model
    def default_appointment_date(self):
        return fields.Datetime.now()

    @api.model
    def default_institution(self):
        return self.env['res.partner'].get_institution()

    name = fields.Char(
        'Appointment ID',
        readonly=True
    )

    patient = fields.Many2one(
        'medical.patient',
        'Patient',
        index=True,
        help='Patient Name'
    )

    healthprof = fields.Many2one(
        'res.partner',
        'Health Prof',
        index=True,
        domain=[('is_healthprof', '=', True)],
        help='Health Professional'
    )

    appointment_date = fields.Datetime(
        'Date and Time',
        default=default_appointment_date
    )

    checked_in_date = fields.Datetime(
        'Checked-in Time'
    )

    institution = fields.Many2one(
        'res.partner',
        'Institution',
        default=default_institution,
        domain=[('is_institution', '=', True)],
        help='Health Care Institution'
    )

    speciality = fields.Many2one(
        'medical.specialty',
        'Specialty',
        help='Medical Specialty / Sector'
    )

    state = fields.Selection(
        [
            ('none', ''),
            ('free', 'Free'),
            ('confirmed', 'Confirmed'),
            ('checked_in', 'Checked in'),
            ('done', 'Done'),
            ('user_cancelled', 'Cancelled by patient'),
            ('center_cancelled', 'Cancelled by Health Center'),
            ('no_show', 'No show')
        ],
        'State',
        default='confirmed',
        sort=False
    )

    urgency = fields.Selection(
        [
            ('none', ''),
            ('a', 'Normal'),
            ('b', 'Urgent'),
            ('c', 'Medical Emergency'),
        ],
        'Urgency',
        default='a',
        sort=False
    )

    comments = fields.Text(
        'Comments'
    )

    appointment_type = fields.Selection(
        [
            ('none', ''),
            ('outpatient', 'Outpatient'),
            ('inpatient', 'Inpatient'),
        ],
        'Type',
        default='outpatient',
        sort=False
    )

    visit_type = fields.Selection(
        [
            ('none', ''),
            ('new', 'New health condition'),
            ('followup', 'Followup'),
            ('well_child', 'Well Child visit'),
            ('well_woman', 'Well Woman visit'),
            ('well_man', 'Well Man visit'),
        ],
        'Visit',
        sort=False
    )

    consultations = fields.Many2one(
        'product.product', 'Consultation Services',
        domain=[('type', '=', 'service')],
        help='Consultation Services'
    )

    def checked_in(self):
        self.ensure_one()
        self.write({'state': 'checked_in'})

    def no_show(self):
        self.ensure_one()
        self.write({'state': 'no_show'})

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if operator.startswith('!') or operator.startswith('not '):
            domain = [('name', operator, name),
                      ('patient.name', operator, name)]
        else:
            domain = ['|', '|',
                      ('name', operator, name),
                      ('patient.name', operator, name)]
        rec = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(rec).with_user(name_get_uid))

    @api.model_create_multi
    def create(self, vals_list):

        vals_list = [x.copy() for x in vals_list]
        for values in vals_list:
            if values['state'] == 'confirmed' and not values.get('name'):
                values['name'] = self.env['ir.sequence'].next_by_code('medical.appointment')

        return super(Appointment, self).create(vals_list)

    def write(self, values):

        if values.get('state') == 'confirmed' and not values.get('name'):
            values['name'] = self.env['ir.sequence'].next_by_code('medical.appointment')

        # Update the checked-in time only if unset
        if values.get('state') == 'checked_in' \
                and values.get('checked_in_date') is None:
            values['checked_in_date'] = fields.Datetime.now()

        return super(Appointment, self).write(values)

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        if default is None:
            default = {}
        default = default.copy()
        default['name'] = None
        default['appointment_date'] = self.default_appointment_date()
        default['state'] = 'confirmed'
        return super(Appointment, self).copy(default)

    @api.depends('patient')
    def on_change_patient(self):
        if self.patient:
            self.state = 'confirmed'
        else:
            self.state = 'free'

