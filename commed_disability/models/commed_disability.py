# -*- coding: utf-8 -*-
from odoo import models, fields, api


class CommedPatient(models.Model):
    _inherit = 'commed.patient'

    disability = fields.Boolean('Disabilities / Barriers',
                                default=False,
                                help="Mark this "
                                "box if the patient has history of significant disabilities and/or "
                                "barriers. Review the Disability Assessments, socioeconomic info,  "
                                "diseases and surgeries for more details")

    uxo = fields.Boolean('UXO',
                         default=False,
                         help="UXO casualty")

    amputee = fields.Boolean('Amputee',
                             default=False,
                             help="Person has had one or more"
                                  " limbs removed by amputation. Includes congenital conditions")

    amputee_since = fields.Date('Since',
                                default=fields.Date.today(),
                                help="Date of amputee status")
    
    amputations = fields.One2many('commed.patient.amputation',
                                  'patient',
                                  'Amputations')

    protheses = fields.One2many('commed.patient.prothesis',
                                'patient',
                                'Protheses')


class Product(models.Model):
    _inherit = 'product.product'

    is_prothesis = fields.Boolean(
        'Prothesis',
        default=False,
        help='Check if the product is a prothesis')


class BodyFunctionCategory(models.Model):
    _name = 'commed.body_function.category'
    _description = 'Body Function Category'

    name = fields.Char('Name',
                       required=True,
                       index=True)

    code = fields.Char('Code',
                       required=True,
                       index=True)

    _sql_constraints = [
        (
            'unique_code',
            'unique(code)',
            'The code must be unique !'
        )
    ]


class BodyFunction(models.Model):
    _name = 'commed.body_function'
    _description = 'Body Functions'

    name = fields.Char('Function',
                       required=True,
                       index=True)
    code = fields.Char('Code',
                       required=True,
                       index=True)
    category = fields.Many2one('commed.body_function.category',
                               'Category')

    _sql_constraints = [
        (
            'unique_code',
            'unique(code)',
            'The code must be unique !'
        )
    ]


class BodyStructureCategory(models.Model):
    _name = 'commed.body_structure.category'
    _description = 'Body Structure Category'

    name = fields.Char('Name',
                       required=True,
                       index=True)

    code = fields.Char('Code',
                       index=True,
                       required=True)

    _sql_constraints = [
        (
            'unique_code',
            'unique(code)',
            'The code must be unique !'
        )
    ]


class BodyStructure(models.Model):
    _name = 'commed.body_structure'
    _description = 'Body Structure'

    name = fields.Char('Structure',
                       required=True,
                       index=True)
    code = fields.Char('Code',
                       required=True,
                       index=True)
    category = fields.Many2one('commed.body_structure.category',
                               'Category')

    _sql_constraints = [
        (
            'unique_code',
            'unique(code)',
            'The code must be unique !'
        )
    ]


class ActivityAndParticipationCategory(models.Model):
    _name = 'commed.activity_and_participation.category'
    _description = 'Activity and Participation Category'

    name = fields.Char('Name',
                       required=True,
                       index=True)
    code = fields.Char('Code',
                       required=True,
                       index=True)

    _sql_constraints = [
        (
            'unique_code',
            'unique(code)',
            'The code must be unique !'
        )
    ]
    

class ActivityAndParticipation(models.Model):
    _name = 'commed.activity_and_participation'
    _description = 'Activity limitations and participation restrictions'

    name = fields.Char('A & P',
                       required=True,
                       index=True)
    code = fields.Char('Code',
                       required=True,
                       index=True)
    category = fields.Many2one(
        'commed.activity_and_participation.category',
        'Category')

    _sql_constraints = [
        (
            'unique_code',
            'unique(code)',
            'The code must be unique !'
        )
    ]


class EnvironmentalFactorCategory(models.Model):
    _name = 'commed.environmental_factor.category'
    _description = 'Environmental Factor Category'

    name = fields.Char('Name',
                       required=True,
                       index=True)
    code = fields.Char('Code',
                       required=True,
                       index=True)
    _sql_constraints = [
        (
            'unique_code',
            'unique(code)',
            'The code must be unique !'
        )
    ]


class EnvironmentalFactor(models.Model):
    _name = 'commed.environmental_factor'
    _description = 'Environmental factors restrictions'

    name = fields.Char('Environment',
                       required=True,
                       index=True)
    code = fields.Char('Code',
                       required=True,
                       index=True)
    category = fields.Many2one(
        'commed.environmental_factor.category',
        'Category')

    _sql_constraints = [
        (
            'unique_code',
            'unique(code)',
            'The code must be unique !'
        )
    ]


class PatientDisabilityAssessment(models.Model):
    _name = 'commed.patient.disability_assessment'
    _description = 'Patient Disability Information'
    _rec_name = "assessment"


    patient = fields.Many2one('commed.patient',
                              'Patient',
                              required=True)
    assessment_date = fields.Date('Date',
                                  default=fields.Date.today())

    assessment = fields.Char('Code')

    crutches = fields.Boolean('Crutches',
                              default=False)
    wheelchair = fields.Boolean('Wheelchair',
                                default=False)

    uxo = fields.Boolean('UXO',
                         compute="get_uxo_status",
                         help="UXO casualty")

    amputee = fields.Boolean('Amputee',
                             compute="get_amputee_status",
                             help="Person has had one or more"
                             " limbs removed by amputation. Includes congenital conditions")

    amputee_since = fields.Date('Since',
                                compute="get_amputee_date",
                                help="Date of amputee status")

    notes = fields.Text('Notes',
                        help="Extra Information")

    hand_function = fields.Selection([
        ('None', ''),
        ('0', 'No impairment'),
        ('1', 'Mild impairment'),
        ('2', 'Moderate impairment'),
        ('3', 'Severe impairment'),
        ('4', 'Complete impairment'),
        ],
        'Hand',
        sort=False)

    visual_function = fields.Selection([
        ('None', ''),
        ('0', 'No impairment'),
        ('1', 'Mild impairment'),
        ('2', 'Moderate impairment'),
        ('3', 'Severe impairment'),
        ('4', 'Complete impairment'),
        ],
        'Visual',
        sort=False)

    speech_function = fields.Selection([
        ('None', ''),
        ('0', 'No impairment'),
        ('1', 'Mild impairment'),
        ('2', 'Moderate impairment'),
        ('3', 'Severe impairment'),
        ('4', 'Complete impairment'),
        ],
        'Speech',
        sort=False)

    hearing_function = fields.Selection([
        ('None', ''),
        ('0', 'No impairment'),
        ('1', 'Mild impairment'),
        ('2', 'Moderate impairment'),
        ('3', 'Severe impairment'),
        ('4', 'Complete impairment'),
        ],
        'Hearing',
        sort=False)

    cognitive_function = fields.Selection([
         ('None', ''),
        ('0', 'No impairment'),
        ('1', 'Mild impairment'),
        ('2', 'Moderate impairment'),
        ('3', 'Severe impairment'),
        ('4', 'Complete impairment'),
        ],
        'Cognitive',
        sort=False)

    locomotor_function = fields.Selection([
        ('None', ''),
        ('0', 'No impairment'),
        ('1', 'Mild impairment'),
        ('2', 'Moderate impairment'),
        ('3', 'Severe impairment'),
        ('4', 'Complete impairment'),
        ],
        'Mobility',
        sort=False)

    activity_participation = fields.Selection([
        ('None', ''),
        ('0', 'No impairment'),
        ('1', 'Mild impairment'),
        ('2', 'Moderate impairment'),
        ('3', 'Severe impairment'),
        ('4', 'Complete impairment'),
        ],
        'A & P',
        sort=False)

    body_functions = fields.One2many('commed.body_function.assessment',
                                     'assessment',
                                     'Body Functions Impairments')

    body_structures = fields.One2many('commed.body_structure.assessment',
                                      'assessment',
                                      'Body Structures Impairments')

    activity_and_participation = fields.One2many(
        'commed.activity.assessment',
        'assessment',
        'Activities and Participation Impairments')

    environmental_factor = fields.One2many(
        'commed.environment.assessment',
        'assessment',
        'Environmental Factors Barriers')

    professional = fields.Many2one(
       'res.partner',
       'Health Professional',
       help="Authorized health professional",
    )

    company_id = fields.Many2one('res.company',
                                 string='Company',
                                 index=True,
                                 required=True,
                                 default=lambda self: self.env.company.id)
    user_id = fields.Many2one(
                             'res.users',
                             "Approved by",
                             default=lambda self: self.env.uid,
                             readonly=True,
                             copy=False)

    @api.depends('patient')
    def get_uxo_status(self):
        for record in self:
            if record.patient:
                record.uxo = record.patient.uxo
            else:
                record.uxo = False

    @api.depends('patient')
    def get_amputee_status(self):
        for record in self:
            if record.patient:
                record.amputee = record.patient.amputee
            else:
                record.amputee = False

    @api.depends('patient')
    def get_amputee_date(self):
        for record in self:
            if record.patient:
                record.amputee_since = record.patient.amputee_since
            else:
                record.amputee_since = False


class PatientBodyFunctionAssessment(models.Model):
    _name = 'commed.body_function.assessment'
    _description = 'Body Functions Assessment'
    _rec_name = 'display_name'

    assessment = fields.Many2one('commed.patient.disability_assessment',
                                 'Assessment',
                                 required=True)

    body_function = fields.Many2one(
        'commed.body_function',
        'Body Function')

    qualifier = fields.Selection([
        ('None', ''),
        ('0', 'No impairment'),
        ('1', 'Mild impairment'),
        ('2', 'Severe impairment'),
        ('3', 'Complete impairment'),
        ('8', 'Not specified'),
        ('9', 'Not applicable'),
        ],
        'Qualifier',
        sort=False)

    company_id = fields.Many2one('res.company',
                                 string='Company',
                                 index=True,
                                 required=True,
                                 default=lambda self: self.env.company.id)

    display_name = fields.Char(compute="set_display_name",
                               string="Name",
                               store=True)

    @api.depends("assessment")
    def set_display_name(self):
        self.display_name = self.assessment.assessment

    @api.depends("assessment")
    def set_display_name(self):
        self.display_name = self.assessment.assessment


class PatientBodyStructureAssessment(models.Model):
    _name = 'commed.body_structure.assessment'
    _description = 'Body Functions Assessment'
    _rec_name = 'display_name'

    assessment = fields.Many2one('commed.patient.disability_assessment',
                                 'Assessment',
                                 required=True)
    body_structure = fields.Many2one('commed.body_structure',
                                     'Body Structure')

    qualifier1 = fields.Selection([
        ('None', ''),
        ('0', 'No impairment'),
        ('1', 'Mild impairment'),
        ('2', 'Moderate impairment'),
        ('3', 'Severe impairment'),
        ('4', 'Complete impairment'),
        ('8', 'Not specified'),
        ('9', 'Not applicable'),
        ],
        'Extent',
        help="Extent of the impairment",
        sort=False)

    qualifier2 = fields.Selection([
        ('None', ''),
        ('0', 'No change in structure'),
        ('1', 'Total absence'),
        ('2', 'Partial absence'),
        ('3', 'Additional part'),
        ('4', 'Aberrant dimensions'),
        ('5', 'Discontinuity'),
        ('6', 'Deviating position'),
        ('7', 'Qualitative changes in structure, including accumulation of fluid'),
        ('8', '8 - Not specified'),
        ('9', '9 - Not applicable'),
        ],
        'Nature',
        help="Nature of the change",
        sort=False)

    body_side = fields.Selection([
        ('None', ''),
        ('left', 'Left'),
        ('right', 'Right'),
        ('both', 'Both'),
        ], 'Side',
        help="Side of the body, if applies",
        sort=False)

    company_id = fields.Many2one('res.company',
                                 string='Company',
                                 index=True,
                                 required=True,
                                 default=lambda self: self.env.company.id)

    display_name = fields.Char(compute="set_display_name",
                               string="Name",
                               store=True)

    @api.depends("assessment")
    def set_display_name(self):
        self.display_name = self.assessment.assessment

    @api.depends("assessment")
    def set_display_name(self):
        self.display_name = self.assessment.assessment


class PatientActivityAndParticipationAsssessment(models.Model):
    _name = 'commed.activity.assessment'
    _description = 'Activity and Participation Assessment'

    assessment = fields.Many2one('commed.patient.disability_assessment',
                                 'Assessment',
                                 required=True)

    activity_and_participation = fields.Many2one(
        'commed.activity_and_participation',
        'Activity')

    qualifier1 = fields.Selection([
        ('None', ''),
        ('0', 'No difficulty'),
        ('1', 'Mild difficulty'),
        ('2', 'Moderate difficulty'),
        ('3', 'Severe difficulty'),
        ('4', 'Complete difficulty'),
        ('8', 'Not specified'),
        ('9', 'Not applicable'),
        ],
        'Performance',
        help="Extent of the difficulty",
        sort=False)

    qualifier2 = fields.Selection([
        ('None', ''),
        ('0', 'No difficulty'),
        ('1', 'Mild difficulty'),
        ('2', 'Moderate difficulty'),
        ('3', 'Severe difficulty'),
        ('4', 'Complete difficulty'),
        ('8', 'Not specified'),
        ('9', 'Not applicable'),
        ], 'Capacity',
        help="Extent of the dificulty",
        sort=False)

    company_id = fields.Many2one('res.company',
                                 string='Company',
                                 index=True,
                                 required=True,
                                 default=lambda self: self.env.company.id)

    display_name = fields.Char(compute="set_display_name",
                               string="Name",
                               store=True)

    @api.depends("assessment")
    def set_display_name(self):
        self.display_name = self.assessment.assessment


class PatientEnvironmentalFactorAssessment(models.Model):
    _name = 'commed.environment.assessment'
    _description = 'Environmental Factors Assessment'
    _rec_name = 'display_name'

    assessment = fields.Many2one('commed.patient.disability_assessment',
                                 'Assessment',
                                 required=True)

    environmental_factor = fields.Many2one(
        'commed.environmental_factor',
        'Environment')

    qualifier = fields.Selection([
        ('None', ''),
        ('0', 'No barriers'),
        ('1', 'Mild barriers'),
        ('2', 'Moderate barriers'),
        ('3', 'Severe barriers'),
        ('4', 'Complete barriers'),
        ('00', 'No facilitator'),
        ('11', 'Mild facilitator'),
        ('22', 'Moderate facilitator'),
        ('33', 'Severe facilitator'),
        ('44', 'Complete facilitator'),
        ], 'Barriers',
        help="Extent of the barriers or facilitators",
        sort=False)

    company_id = fields.Many2one('res.company',
                                 string='Company',
                                 index=True,
                                 required=True,
                                 default=lambda self: self.env.company.id)

    display_name = fields.Char(compute="set_display_name",
                               string="Name",
                               store=True)

    @api.depends("assessment")
    def set_display_name(self):
        self.display_name = self.assessment.assessment


class PatientAmputation(models.Model):
    _name = 'commed.patient.amputation'
    _description = 'Amputation'
    _rec_name = 'display_name'

    patient = fields.Many2one('commed.patient',
                              'Patient',
                              required=True)

    amputation_date = fields.Date('Date')

    body_structure = fields.Many2one('commed.body_structure',
                                     'Structure')

    etiology = fields.Selection([
        ('None', ''),
        ('pvd', 'Peripherial Vascular Disease'),
        ('trauma', 'Trauma'),
        ('neoplasia', 'Neoplasia'),
        ('infection', 'Infection'),
        ('congenital', 'Congenital'),
        ], 'Etiology',
        sort=False)

    limb = fields.Selection([
        ('None', ''),
        ('lower', 'lower limb'),
        ('upper', 'upper limb'),
        ], 'Limb',
        sort=False)

    side = fields.Selection([
        ('None', ''),
        ('left', 'left'),
        ('right', 'right'),
        ('both', 'both'),
        ], 'Side',
        sort=False)

    amputation_level = fields.Selection([
        ('None', ''),
        ('sd', 'SD - Shoulder disarticulation'),
        ('th', 'TH - Transhumeral'),
        ('ed', 'ED - Elbow disarticulation'),
        ('tr', 'TR - Transradial'),
        ('wd', 'WD - Wrist disarticulation'),
        ('ph', 'PH'),
        ('hp', 'HD - Hemipelvectomy'),
        ('tf', 'TF - Transfemoral'),
        ('tt', 'TT - Transtibial'),
        ('symes', 'Symes'),
        ('pffd', 'PFFD'),
        ], 'Level',
        sort=False)

    comments = fields.Char('Comments')

    professional = fields.Many2one(
       'res.partner',
       'Health Professional',
       readonly=True,
    )

    company_id = fields.Many2one('res.company',
                                 string='Company',
                                 index=True,
                                 required=True,
                                 default=lambda self: self.env.company.id)

    display_name = fields.Char(compute="set_display_name",
                               string="Name",
                               store=True)

    user_id = fields.Many2one(
                             'res.users',
                             "Approved by",
                             default=lambda self: self.env.uid,
                             readonly=True,
                             copy=False)

    @api.depends("patient")
    def set_display_name(self):
        self.display_name = self.patient.name


class PatientProthesis(models.Model):
    _name = 'commed.patient.prothesis'
    _description = 'Prothesis'
    _rec_name = 'display_name'

    patient = fields.Many2one('commed.patient',
                              'Patient',
                              required=True)

    issue_date = fields.Date('Date')

    prothesis = fields.Many2one(
        'product.product',
        'Prothesis', required=True,
        domain=[('is_prothesis', '=', True)],
        help='Prosthetic device')

    comments = fields.Char('Comments')

    professional = fields.Many2one(
       'res.partner',
       'Health Professional',
       readonly=True,
    )

    user_id = fields.Many2one(
                             'res.users',
                             "Approved by",
                             default=lambda self: self.env.uid,
                             readonly=True,
                             copy=False)

    company_id = fields.Many2one('res.company',
                                 string='Company',
                                 index=True,
                                 required=True,
                                 default=lambda self: self.env.company.id)

    display_name = fields.Char(compute="set_display_name",
                               string="Name",
                               store=True)

    @api.depends("patient")
    def set_display_name(self):
        self.display_name = self.patient.name


class PatientData(models.Model):
    _inherit = 'commed.patient'

    disability_assesments = fields.One2many('commed.patient.disability_assessment',
                                            'patient',
                                            'Assessment',
                                            readonly=True)






