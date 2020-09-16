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

    critical_summary = fields.Text(
        'Important health conditions related to this patient',
        help='Automated summary of patient important health conditions '
        'other critical information')

    critical_info = fields.Text(
        'Free text information not included in the automatic summary',
        help='Write any important information on the patient\'s condition,'
        ' surgeries, allergies, ...')


class MedicalInstitution(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    def get_institution(self):
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


class MedicalSpecialty(models.Model):
    _name = 'medical.specialty'
    _description = 'Medical Specialty'

    name = fields.Char(
        'Specialty',
        required=True,
        translate=True,
        help='ie, Addiction Psychiatry'
    )
    code = fields.Char(
        'Code',
        required=True,
        help='ie, ADP. Please use CAPITAL LETTERS and no spaces'
    )

    _sql_constraints = [
        ('code_uniq', 'unique (code)', 'The CODE must be unique!'),
        ('name_uniq', 'unique (name)', 'The Specialty must be unique!'),
    ]


# gnuhealth.healthprofessional
class HealthProfessional(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    def default_institution(self):
        return self.env['res.partner'].get_institution()

    def get_health_professional(self):
        # Get the professional associated to the internal user id
        # that logs into GNU Health
        if self.env.user and self.env.user.partner_id.is_healthprof:
            return self.env.user.partner_id.is_healthprof
        else:
            raise UserError(
                _(
                    'No Health Professional associated to this user!'
                ))

    institution = fields.Many2one(
        'res.partner',
        'Institution',
        domain=[('is_institution', '=', True)],
        default=default_institution,
        help='Main institution where she/he works'
    )

    code_healthprof = fields.Char(
        'LICENSE ID',
        help='License ID'
    )

    specialties = fields.One2many(
        'medical.hp_specialty',
        'name',
        'Specialties'
    )

    is_healthprof = fields.Boolean(
        'Health Professional',
        index=True
    )

    _sql_constraints = [
        ('code_uniq', 'unique (code_healthprof)', 'The CODE must be unique!'),
        ('name_uniq', 'unique (name)', 'The health professional must be unique!'),
    ]


class HealthProfessionalSpecialties(models.Model):
    _name = 'medical.hp_specialty'
    _description = 'Health Professional Specialties'

    name = fields.Many2one(
        'res.partner',
        'Health Professional',
        domain=[('is_healthprof', '=', True)],
        required=True
    )

    specialty = fields.Many2one(
        'medical.specialty',
        'Specialty',
        required=True,
        help='Specialty Code'
    )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'This specialty is already assigned to the Health Professional!'),
    ]


class HospitalBed(models.Model):
    _name = 'medical.hospital.bed'
    _description = 'Hospital Bed'
    _rec_name = 'telephone_number'

    def default_institution(self):
        return self.env['res.partner'].get_institution()

    name = fields.Many2one(
        'product.product',
        'Bed',
        required=True,
        domain=[('is_bed', '=', True)],
        help='Bed Number'
    )

    institution = fields.Many2one(
        'res.partner',
        'Institution',
        domain=[('is_institution', '=', True)],
        required=True,
        help='Health Institution',
        default=default_institution,
    )

    # ward = fields.Many2one(
    #     'gnuhealth.hospital.ward',
    #     'Ward',
    #     domain=[('institution', '=', Eval('institution'))],
    #     depends=['institution'],
    #     help='Ward or room'
    # )

    bed_type = fields.Selection(
        [
            ('none', ''),
            ('gatch', 'Gatch Bed'),
            ('electric', 'Electric'),
            ('stretcher', 'Stretcher'),
            ('low', 'Low Bed'),
            ('low_air_loss', 'Low Air Loss'),
            ('circo_electric', 'Circo Electric'),
            ('clinitron', 'Clinitron'),
        ],
        'Bed Type',
        required=True,
        default='gatch',
        sort=False)

    telephone_number = fields.Char(
        'Telephone Number',
        help='Telephone number / Extension'
    )

    extra_info = fields.Text(
        'Extra Info'
    )

    state = fields.Selection(
        [
            ('none', ''),
            ('free', 'Free'),
            ('reserved', 'Reserved'),
            ('occupied', 'Occupied'),
            ('to_clean', 'Needs cleaning'),
            ('na', 'Not available'),
        ],
        'Status',
        readonly=True,
        default='free',
        sort=False
    )

    def fix_bed(self):
        self.write({'state': 'free'})

    _sql_constraints = [
        ('name_uniq', 'unique (name, institution)', 'The Bed must be unique per Health Center!'),
    ]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_medicament = fields.Boolean(
        'Medicament',
        help='Check if the product is a medicament'
    )
    is_medical_supply = fields.Boolean(
        'Medical Supply',
        help='Check if the product is a medical supply'
    )
    is_vaccine = fields.Boolean(
        'Vaccine',
        help='Check if the product is a vaccine'
    )
    is_bed = fields.Boolean(
        'Bed',
        help='Check if the product is a bed on the gnuhealth.center'
    )
    is_insurance_plan = fields.Boolean(
        'Insurance Plan',
        help='Check if the product is an insurance plan'
    )


class MedicamentCategory(models.Model):
    _name = 'medical.medicament.category'
    _description = 'Medicament Category'
    _parent_name = "parent_id"
    _parent_store = True

    name = fields.Char(
        'Name',
        required=True,
        translate=True
    )

    complete_name = fields.Char(
        'Complete Name',
        compute='_compute_complete_name',
        store=True
    )

    parent_path = fields.Char(
        index=True
    )

    parent_id = fields.Many2one(
        'medical.medicament.category',
        'Parent Category',
        index=True
    )

    child_ids = fields.One2many(
        'medical.medicament.category',
        'parent_id',
        string='Children'
    )

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    @api.model
    def name_create(self, name):
        return self.create({'name': name}).name_get()[0]


class Medicament(models.Model):
    _name = 'medical.medicament'
    _description = 'Medicament'

    name = fields.Many2one(
        'product.product',
        'Product',
        required=True,
        domain=[('is_medicament', '=', True)],
        help='Product Name'
    )

    active_component = fields.Char(
        'Active component',
        translate=True,
        help='Active Component'
    )

    category = fields.Many2one(
        'medical.medicament.category',
        'Category',
        index=True)

    therapeutic_action = fields.Char(
        'Therapeutic effect',
        help='Therapeutic action'
    )

    composition = fields.Text(
        'Composition',
        help='Components'
    )
    indications = fields.Text(
        'Indication',
        help='Indications'
    )
    strength = fields.Float(
        'Strength',
        help='Amount of medication (eg, 250 mg) per dose'
    )

    unit = fields.Many2one(
        'medical.dose.unit',
        'dose unit',
        help='Unit of measure for the medication to be taken'
    )

    route = fields.Many2one(
        'medical.drug.route',
        'Administration Route',
        help='Drug administration route code.'
    )

    form = fields.Many2one(
        'medical.drug.form',
        'Form',
        help='Drug form, such as tablet, suspension, liquid ..'
    )

    sol_conc = fields.Float(
        'Concentration',
        help='Solution drug concentration'
    )

    sol_conc_unit = fields.Many2one(
        'medical.dose.unit',
        'Unit',
        help='Unit of the drug concentration'
    )

    sol_vol = fields.Float(
        'Volume',
        help='Solution concentration volume'
    )

    sol_vol_unit = fields.Many2one(
        'medical.dose.unit', 'Unit',
        help='Unit of the solution volume'
    )

    dosage = fields.Text(
        'Dosage Instructions',
        help='Dosage / Indications'
    )
    overdosage = fields.Text(
        'Overdosage',
        help='Overdosage'
    )
    pregnancy_warning = fields.Boolean(
        'Pregnancy Warning',
        help='The drug represents risk to pregnancy or lactancy'
    )

    pregnancy = fields.Text(
        'Pregnancy and Lactancy',
        help='Warnings for Pregnant Women'
    )

    pregnancy_category = fields.Selection(
        [
            ('none', ''),
            ('A', 'A'),
            ('B', 'B'),
            ('C', 'C'),
            ('D', 'D'),
            ('X', 'X'),
            ('N', 'N'),
        ],
        'Pregnancy Category',
        help='** FDA Pregnancy Categories ***\n'
             'CATEGORY A :Adequate and well-controlled human studies have failed'
             ' to demonstrate a risk to the fetus in the first trimester of'
             ' pregnancy (and there is no evidence of risk in later'
             ' trimesters).\n\n'
             'CATEGORY B : Animal reproduction studies have failed todemonstrate a'
             ' risk to the fetus and there are no adequate and well-controlled'
             ' studies in pregnant women OR Animal studies have shown an adverse'
             ' effect, but adequate and well-controlled studies in pregnant women'
             ' have failed to demonstrate a risk to the fetus in any'
             ' trimester.\n\n'
             'CATEGORY C : Animal reproduction studies have shown an adverse'
             ' effect on the fetus and there are no adequate and well-controlled'
             ' studies in humans, but potential benefits may warrant use of the'
             ' drug in pregnant women despite potential risks. \n\n '
             'CATEGORY D : There is positive evidence of human fetal  risk based'
             ' on adverse reaction data from investigational or marketing'
             ' experience or studies in humans, but potential benefits may warrant'
             ' use of the drug in pregnant women despite potential risks.\n\n'
             'CATEGORY X : Studies in animals or humans have demonstrated fetal'
             ' abnormalities and/or there is positive evidence of human fetal risk'
             ' based on adverse reaction data from investigational or marketing'
             ' experience, and the risks involved in use of the drug in pregnant'
             ' women clearly outweigh potential benefits.\n\n'
             'CATEGORY N : Not yet classified'
    )

    presentation = fields.Text(
        'Presentation',
        help='Packaging'
    )
    adverse_reaction = fields.Text(
        'Adverse Reactions'
    )
    storage = fields.Text(
        'Storage Conditions'
    )
    is_vaccine = fields.Boolean(
        'Vaccine'
    )
    notes = fields.Text(
        'Extra Info'
    )

    active = fields.Boolean(
        'Active',
        index=True,
        default=True)
    #
    # # Show the icon depending on the pregnancy category
    # pregnancy_cat_icon = \
    #     fields.Function(fields.Char('Preg. Cat. Icon'), 'get_preg_cat_icon')
    #
    # def get_preg_cat_icon(self, name):
    #     if (self.pregnancy_category == 'X'):
    #         return 'gnuhealth-stop'
    #     if (self.pregnancy_category == 'D' or self.pregnancy_category == "C"):
    #         return 'gnuhealth-warning'


class DrugForm(models.Model):
    _name = 'medical.drug.form'
    _description = 'Drug Form'

    name = fields.Char(
        'Form',
        required=True,
        index=True,
        translate=True
    )
    code = fields.Char(
        'Code',
        required=True,
        help="Please use CAPITAL LETTERS and no spaces"
    )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The Unit must be unique!'),
        ('code_uniq', 'unique (code)', 'The CODE must be unique!'),
    ]


class DrugRoute(models.Model):
    _name = 'medical.drug.route'
    _description = 'Drug Administration Route'

    name = fields.Char(
        'Route',
        required=True,
        index=True,
        translate=True
    )
    code = fields.Char(
        'Code',
        required=True,
        help="Please use CAPITAL LETTERS and no spaces"
    )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The Unit must be unique!'),
        ('code_uniq', 'unique (code)', 'The CODE must be unique!'),
    ]


class DrugDoseUnits(models.Model):
    _name = 'medical.dose.unit'
    _description = 'Drug Dose Unit'

    name = fields.Char(
        'Unit',
        required=True,
        index=True,
        translate=True)

    desc = fields.Char(
        'Description',
        translate=True
    )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The Unit must be unique!'),
    ]
