# -*- coding: utf-8 -*-
from urllib.parse import urlencode
from urllib.parse import urlunparse
from collections import OrderedDict
from io import BytesIO
import platform
import os

try:
    from PIL import Image
except ImportError:
    Image = None

from odoo import fields, models, api, _
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date

from uuid import uuid4
import string
import random
import pytz
def compute_age_from_dates(dob, deceased, dod, gender, caller, extra_date):
    """ Get the person's age.

    Calculate the current age of the patient or age at time of death.

    Returns:
    If caller == 'age': str in Y-M-D,
       caller == 'childbearing_age': boolean,
       caller == 'raw_age': [Y, M, D]

    """
    today = datetime.today().date()

    if dob:
        start = datetime.strptime(str(dob), '%Y-%m-%d')
        end = datetime.strptime(str(today),'%Y-%m-%d')

        if extra_date:
            end = datetime.strptime(str(extra_date), '%Y-%m-%d')

        if deceased and dod:
            end = datetime.strptime(
                        str(dod), '%Y-%m-%d %H:%M:%S')

        rdelta = relativedelta(end, start)


        years_months_days = str(rdelta.years) + 'y ' \
            + str(rdelta.months) + 'm ' \
            + str(rdelta.days) + 'd'

    else:
        return None

    if caller == 'age':
        return years_months_days

    elif caller == 'childbearing_age':
        if (rdelta.years >= 11
            and rdelta.years <= 55 and gender == 'f'):
            return True
        else:
            return False

    elif caller == 'raw_age':
        return [rdelta.years, rdelta.months, rdelta.days]

    else:
        return None


class PatientEvaluation(models.Model):
    _name = 'medical.patient.evaluation'
    _description = 'Patient Evaluation'

    STATES = {'signed': [('readonly', True)]}

    # def patient_age_at_evaluation(self, name):
    #     if (self.patient.name.dob and self.evaluation_start):
    #         return compute_age_from_dates(self.patient.name.dob, None,
    #                     None, None, 'age', self.evaluation_start.date())

    def evaluation_duration(self, name):
        if (self.evaluation_endtime and self.evaluation_start):
            return self.evaluation_endtime - self.evaluation_start

    def get_wait_time(self, name):
        # Compute wait time between checked-in and start of evaluation
        if self.appointment:
            if self.appointment.checked_in_date:
                if self.appointment.checked_in_date < self.evaluation_start:
                    return self.evaluation_start-self.appointment.checked_in_date

    code = fields.Char('Code',
        help="Unique code that \
        identifies the evaluation")

    patient = fields.Many2one('medical.patient',
        string='Patient')

    appointment = fields.Many2one(
        'medical.appointment',
        'Appointment',
        domain=[('patient', '=', 'patient')],
        depends=['patient'],
        help='Enter or select the date / ID of the appointment related to'
        ' this evaluation',
        states = STATES)

    # related_condition = fields.Many2one('gnuhealth.patient.disease', 'Related condition',
    #     domain=[('name', '=', 'patient')], depends=['patient'],
    #     help="Related condition related to this follow-up evaluation",

    evaluation_start = fields.Datetime('Start',
        required=True)

    evaluation_endtime = fields.Datetime('End')

    evaluation_length = fields.Datetime(
            'Evaluation length',
            help="Duration of the evaluation",compute='evaluation_duration')

    wait_time = fields.Datetime('Patient wait time',
        help="How long the patient waited",
        compute='get_wait_time')

    state = fields.Selection([

        ('in_progress', 'In progress'),
        ('done', 'Done'),
        ('signed', 'Signed'),
        ], 'State',
        default='in_progress', readonly=True, sort=False)

    next_evaluation = fields.Many2one(
        'medical.appointment',
        'Next Appointment',
        domain=[('patient', '=', 'patient')],
        depends=['patient'],
        states = STATES)

    user_id = fields.Many2one('res.user', 'Last Changed by', readonly=True)

    # healthprof = fields.Many2one(
    #     'medical.healthprofessional', 'Health Prof',
    #     help="Health professional that initiates the evaluation."
    #     "This health professional might or might not be the same that"
    #     " signs and finishes the evaluation."
    #     "The evaluation remains in progress state until it is signed"
    #     ", when it becomes read-only", readonly=True)
    #
    # signed_by = fields.Many2one(
    #     'medical.healthprofessional', 'Health Prof', readonly=True,
    #     #states={'invisible': Equal(Eval('state'), 'in_progress')},
    #     help="Health Professional that finished the patient evaluation")

    specialty = fields.Many2one('medical.specialty', 'Specialty',
        states = STATES)

    visit_type = fields.Selection([

        ('new', 'New health condition'),
        ('followup', 'Followup'),
        ('well_child', 'Well Child visit'),
        ('well_woman', 'Well Woman visit'),
        ('well_man', 'Well Man visit'),
        ], 'Visit', sort=False)

    urgency = fields.Selection([

        ('a', 'Normal'),
        ('b', 'Urgent'),
        ('c', 'Medical Emergency'),
        ], 'Urgency', sort=False,
        states = STATES)

    computed_age = fields.Char(
            'Age',
            help="Computed patient age at the moment of the evaluation")

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ], 'Gender', compute='get_patient_gender')

    information_source = fields.Char(
        'Source', help="Source of"
        "Information, eg : Self, relative, friend ...")

    reliable_info = fields.Boolean(
        'Reliable', help="Uncheck this option"
        "if the information provided by the source seems not reliable")

    # derived_from = fields.Many2one(
    #     'medical.healthprofessional', 'Derived from',
    #     help='Health Professional who derived the case',
    #     states = STATES)

    # derived_to = fields.Many2one(
    #     'medical.healthprofessional', 'Derived to',
    #     help='Health Professional to derive the case',
    #     states = STATES)

    evaluation_type = fields.Selection([

        ('outpatient', 'Outpatient'),
        ('inpatient', 'Inpatient'),
        ], 'Type', sort=False,
        states = STATES)

    chief_complaint = fields.Char('Chief Complaint', help='Chief Complaint')

    notes_complaint = fields.Text('Complaint details')

    present_illness = fields.Text('Present Illness')

    evaluation_summary = fields.Text('Clinical and physical')

    glycemia = fields.Float(
        'Glycemia',
        help='Last blood glucose level. Can be approximative. Expressed in mg/dL or mmol/L.',
        states = STATES)

    hba1c = fields.Float(
        'Glycated Hemoglobin',
        help='Last Glycated Hb level. Can be approximative. Expressed in mmol/mol.',
        states = STATES)

    cholesterol_total = fields.Integer(
        'Last Cholesterol',
        help='Last cholesterol reading. Can be approximative. Expressed in mg/dL or mmol/L.',
        states = STATES)

    hdl = fields.Integer(
        'Last HDL',
        help='Last HDL Cholesterol reading. Can be approximative. Expressed in mg/dL or mmol/L.',
        states = STATES)

    ldl = fields.Integer(
        'Last LDL',
        help='Last LDL Cholesterol reading. Can be approximative. Expressed in mg/dL or mmol/L.',
        states = STATES)

    tag = fields.Integer(
        'Last TAGs',
        help='Triacylglycerol(triglicerides) level. Can be approximative. Expressed in mg/dL or mmol/L.',
        states = STATES)

    systolic = fields.Integer('Systolic Pressure',
        help='Systolic pressure expressed in mmHg',
        states = STATES)

    diastolic = fields.Integer('Diastolic Pressure',
        help='Diastolic pressure expressed in mmHg',
        states = STATES)

    bpm = fields.Integer(
        'Heart Rate',
        help='Heart rate expressed in beats per minute',
        states = STATES)

    respiratory_rate = fields.Integer(
        'Respiratory Rate',
        help='Respiratory rate expressed in breaths per minute',
        states = STATES)

    osat = fields.Integer(
        'Oxygen Saturation',
        help='Arterial oxygen saturation expressed as a percentage',
        states = STATES)

    malnutrition = fields.Boolean(
        'Malnutrition',
        help='Check this box if the patient show signs of malnutrition. If'
        ' associated  to a disease, please encode the correspondent disease'
        ' on the patient disease history. For example, Moderate'
        ' protein-energy malnutrition, E44.0 in ICD-10 encoding',
        states = STATES)

    dehydration = fields.Boolean(
        'Dehydration',
        help='Check this box if the patient show signs of dehydration. If'
        ' associated  to a disease, please encode the  correspondent disease'
        ' on the patient disease history. For example, Volume Depletion, E86'
        ' in ICD-10 encoding',
        states = STATES)

    temperature = fields.Float(
        'Temperature',
        help='Temperature in celcius',
        states = STATES)

    weight = fields.Float('Weight', digits=(3,2),help='Weight in kilos',
        states = STATES)

    height = fields.Float('Height', digits=(3,1), help='Height in centimeters',
        states = STATES)

    bmi = fields.Float(
        'BMI', digits=(2,2),
        help='Body mass index',
        states = STATES)

    head_circumference = fields.Float(
        'Head',
        help='Head circumference in centimeters',
        states = STATES)

    abdominal_circ = fields.Float('Waist', digits=(3,1),
        help='Waist circumference in centimeters',
        states = STATES)

    hip = fields.Float('Hip', digits=(3,1),
        help='Hip circumference in centimeters',
        states = STATES)

    whr = fields.Float(
        'WHR', digits=(2,2),help='Waist to hip ratio . Reference values:\n'
        'Men : < 0.9 Normal // 0.9 - 0.99 Overweight // > 1 Obesity \n'
        'Women : < 0.8 Normal // 0.8 - 0.84 Overweight // > 0.85 Obesity',
        states = STATES)

    loc = fields.Integer(
        'Glasgow',
        help='Level of Consciousness - on Glasgow Coma Scale :  < 9 severe -'
        ' 9-12 Moderate, > 13 minor',
        states = STATES)

    loc_eyes = fields.Selection([
        ('1', 'Does not Open Eyes'),
        ('2', 'Opens eyes in response to painful stimuli'),
        ('3', 'Opens eyes in response to voice'),
        ('4', 'Opens eyes spontaneously'),
        ], 'Glasgow - Eyes', sort=False,
        states = STATES)

    loc_verbal = fields.Selection([
        ('1', 'Makes no sounds'),
        ('2', 'Incomprehensible sounds'),
        ('3', 'Utters inappropriate words'),
        ('4', 'Confused, disoriented'),
        ('5', 'Oriented, converses normally'),
        ], 'Glasgow - Verbal', sort=False,
        states = STATES)

    loc_motor = fields.Selection([
        ('1', 'Makes no movement'),
        ('2', 'Extension to painful stimuli - decerebrate response -'),
        ('3', 'Abnormal flexion to painful stimuli (decorticate response)'),
        ('4', 'Flexion / Withdrawal to painful stimuli'),
        ('5', 'Localizes painful stimuli'),
        ('6', 'Obeys commands'),
        ], 'Glasgow - Motor', sort=False,
        states = STATES)

    tremor = fields.Boolean(
        'Tremor',
        help='If associated  to a disease, please encode it on the patient'
        ' disease history',
        states = STATES)

    violent = fields.Boolean(
        'Violent Behaviour',
        help='Check this box if the patient is aggressive or violent at the'
        ' moment',
        states = STATES)

    mood = fields.Selection([

        ('n', 'Normal'),
        ('s', 'Sad'),
        ('f', 'Fear'),
        ('r', 'Rage'),
        ('h', 'Happy'),
        ('d', 'Disgust'),
        ('e', 'Euphoria'),
        ('fl', 'Flat'),
        ], 'Mood', sort=False,
        states = STATES)

    orientation = fields.Boolean(
        'Orientation',
        help='Check this box if the patient is disoriented in time and/or'
        ' space',
        states = STATES)

    memory = fields.Boolean(
        'Memory',
        help='Check this box if the patient has problems in short or long'
        ' term memory',
        states = STATES)

    knowledge_current_events = fields.Boolean(
        'Knowledge of Current Events',
        help='Check this box if the patient can not respond to public'
        ' notorious events',
        states = STATES)

    judgment = fields.Boolean(
        'Judgment',
        help='Check this box if the patient can not interpret basic scenario'
        ' solutions',
        states = STATES)

    abstraction = fields.Boolean(
        'Abstraction',
        help='Check this box if the patient presents abnormalities in'
        ' abstract reasoning',
        states = STATES)

    vocabulary = fields.Boolean(
        'Vocabulary',
        help='Check this box if the patient lacks basic intelectual capacity,'
        ' when she/he can not describe elementary objects',
        states = STATES)

    calculation_ability = fields.Boolean(
        'Calculation Ability',
        help='Check this box if the patient can not do simple arithmetic'
        ' problems',
        states = STATES)

    object_recognition = fields.Boolean(
        'Object Recognition',
        help='Check this box if the patient suffers from any sort of gnosia'
        ' disorders, such as agnosia, prosopagnosia ...',
        states = STATES)

    praxis = fields.Boolean(
        'Praxis',
        help='Check this box if the patient is unable to make voluntary'
        'movements',
        states = STATES)

    diagnosis = fields.Many2one(
        'gnuhealth.pathology', 'Main Condition',
        help='Presumptive Diagnosis. If no diagnosis can be made'
        ', encode the main sign or symptom.')

    secondary_conditions = fields.One2many(
        'medical.secondary_condition',
        'evaluation',
        'Other Conditions',
        help='Other '
        ' conditions found on the patient')

    diagnostic_hypothesis = fields.One2many(
        'medical.diagnostic_hypothesis',
        'evaluation', 'Hypotheses / DDx', help='Other Diagnostic Hypotheses /'
        ' Differential Diagnosis (DDx)')

    signs_and_symptoms = fields.One2many(
        'medical.signs_and_symptoms',
        'evaluation', 'Signs and Symptoms', help='Enter the Signs and Symptoms'
        ' for the patient in this evaluation.')

    psychological_assessment = fields.Text("Psychological Assessment")

    info_diagnosis = fields.Text('Presumptive Diagnosis: Extra Info',
        states = STATES)

    directions = fields.Text('Plan')

    actions = fields.One2many(
        'medical.directions', 'name', 'Procedures',
        help='Procedures / Actions to take')

    notes = fields.Text('Notes')

    discharge_reason = fields.Selection([

        ('home', 'Home / Selfcare'),
        ('transfer', 'Transferred to another institution'),
        ('against_advice', 'Left against medical advice'),
        ('death', 'Death')],
        'Discharge Reason', required=True, sort=False,
        # states={'invisible': Equal(Eval('state'), 'in_progress'),
        #     'readonly': Eval('state') == 'signed'},
        help="Reason for patient discharge")

    # institution = fields.Many2one('gnuhealth.institution', 'Institution',
    #     states = STATES)

    report_evaluation_date = fields.Date(
        'Evaluation Date')
    report_evaluation_time = fields.Datetime(
        'Evaluation Time', compute='get_report_evaluation_time')

    # @api.model
    # def default_institution(self):
    #     return HealthInstitution().get_institution()

    @api.model
    def default_discharge_reason(self):
        return 'home'

    @api.depends('patient')
    def get_patient_gender(self):
        self.gender = self.patient.gender

    @api.model
    def search_patient_gender(self, name, clause):
        res = []
        value = clause[2]
        res.append(('patient.name.gender', clause[1], value))
        return res

    @api.model
    def validate(self, evaluations):
        super(PatientEvaluation, self).validate(evaluations)
        for evaluation in evaluations:
            evaluation.validate_evaluation_period()
            evaluation.check_health_professional()

    def validate_evaluation_period(self):
        Lang = self.env['ir.lang']

        language, = Lang.search([
            ('code', '=', self.env.lang),
            ])
        if (self.evaluation_endtime and self.evaluation_start):
            if (self.evaluation_endtime < self.evaluation_start):
                self.raise_user_error('end_date_before_start', {
                        'evaluation_start': Lang.strftime(
                            self.evaluation_start, language.code, language.date),
                        'evaluation_endtime': Lang.strftime(
                            self.evaluation_endtime, language.code, language.date),
                        })

    def check_health_professional(self):
        if not self.healthprof:
            self.raise_user_error('medical_professional_warning')

    # @api.model
    # def default_healthprof(self):
    #
    #     HealthProfessional = self.env['gnuhealth.healthprofessional']
    #     return HealthProfessional.get_health_professional()

    @api.model
    def default_loc_eyes(self):
        return '4'

    @api.model
    def default_loc_verbal(self):
        return '5'

    @api.model
    def default_loc_motor(self):
        return '6'

    @api.model
    def default_loc(self):
        return 15

    @api.model
    def default_evaluation_type(self):
        return 'outpatient'

    @api.model
    def default_state(self):
        return 'in_progress'

    @api.depends('weight', 'height')
    def on_change_with_bmi(self):
        if self.height and self.weight:
            if (self.height > 0):
                return round(self.weight / ((self.height / 100) ** 2),2)
            return 0

    @api.depends('weight', 'height', 'bmi')
    def on_change_bmi(self):
        if self.height and self.weight:
            if (self.height > 0):
                self.bmi = round(self.weight / ((self.height / 100) ** 2),2)
        elif (self.height and not self.weight):
            self.weight = round((((self.height / 100) ** 2) * self.bmi),2)

        elif (self.weight and not self.height):
            self.height = round(((self.weight / self.bmi)**(0.5)*100),2)

    @api.depends('loc_verbal', 'loc_motor', 'loc_eyes')
    def on_change_with_loc(self):
        return int(self.loc_motor) + int(self.loc_eyes) + int(self.loc_verbal)

    # Show the gender and age upon entering the patient
    # These two are function fields (don't exist at DB level)
    @api.depends('patient')
    def on_change_patient(self):
        gender = None
        age = ''
        self.gender = self.patient.gender
        self.computed_age = self.patient.age

    @api.model
    def default_information_source(self):
        return 'Self'

    @api.model
    def default_reliable_info(self):
        return True

    @api.model
    def default_evaluation_start(self):
        return datetime.now()

    # Calculate the WH ratio
    @api.depends('abdominal_circ', 'hip', 'whr')
    def on_change_with_whr(self):
        waist = self.abdominal_circ
        hip = self.hip
        if waist and hip:
            if (hip > 0):
                whr = round((waist / hip),2)
            else:
                whr = 0
            return whr

    def get_rec_name(self, name):
        return str(self.evaluation_start)

    def get_report_evaluation_date(self, name):
        Company = self.env['company.company']

        timezone = None
        company_id = self.env.company
        if company_id:
            company = Company(company_id)
            if company.timezone:
                timezone = pytz.timezone(company.timezone)

        dt = self.evaluation_start
        return datetime.astimezone(dt.replace(tzinfo=pytz.utc), timezone).date()

    def get_report_evaluation_time(self, name):
        Company = self.env['company.company']

        timezone = None
        company_id = self.env.company
        if company_id:
            company = Company(company_id)
            if company.timezone:
                timezone = pytz.timezone(company.timezone)

        dt = self.evaluation_start
        return datetime.astimezone(dt.replace(tzinfo=pytz.utc), timezone).time()

    # @api.model
    # def __setup__(self):
    #     super(PatientEvaluation, self).__setup__()
    #
    #     t = self.__table__()
    #     self._sql_constraints = [
    #         ('code_unique', Unique(t,t.code),
    #             'The evaluation code must be unique !'),
    #         ]
    #
    #     self._order.insert(0, ('evaluation_start', 'DESC'))
    #
    #     self._error_messages.update({
    #         'health_professional_warning':
    #             'No health professional associated to this user',
    #         'end_date_before_start': 'End time "%(evaluation_endtime)s" BEFORE'
    #             ' evaluation start "%(evaluation_start)s"'
    #     })

        # self._buttons.update({
        #     'end_evaluation': {'invisible': Or(Equal(Eval('state'), 'signed'),
        #         Equal(Eval('state'), 'done'))}
        #     })

    # @api.model
    # def create(self, vlist):
    #     Sequence = self.env['ir.sequence']
    #     Config = self.env['gnuhealth.sequences']
    #
    #     vlist = [x.copy() for x in vlist]
    #     for values in vlist:
    #         if not values.get('code'):
    #             config = Config(1)
    #             values['code'] = Sequence.get_id(
    #                 config.patient_evaluation_sequence.id)
    #
    #     return super(PatientEvaluation, self).create(vlist)


    # End the evaluation and discharge the patient

    # def end_evaluation(self, evaluations):
    #
    #     HealthProfessional = self.env['gnuhealth.healthprofessional']
    #     Appointment =self.env['gnuhealth.appointment']
    #
    #     evaluation_id = evaluations[0]
    #
    #     patient_app=[]
    #
    #     # Change the state of the evaluation to "Done"
    #
    #     signing_hp = HealthProfessional.get_health_professional()
    #
    #     self.write(evaluations, {
    #         'state': 'done',
    #         'signed_by': signing_hp,
    #         'evaluation_endtime': datetime.now()
    #         })
    #
    #     # If there is an appointment associated to this evaluation
    #     # set it to state "Done"
    #
    #     if evaluations[0].appointment:
    #         patient_app.append(evaluations[0].appointment)
    #         Appointment.write(patient_app, {
    #             'state': 'done',
    #             })
    #
    #     # Create an entry in the page of life
    #     # It will create the entry at the moment of
    #     # discharging the patient
    #     # The patient needs to have a federation account
    #     if (evaluation_id.patient.name.federation_account):
    #         self.create_evaluation_pol (evaluation_id)

    # @api.model
    # def create_evaluation_pol(self, evaluation):
    #     """ Adds an entry in the person Page of Life
    #         related to this medical evaluation.
    #     """
    #     Pol = self.env['gnuhealth.pol']
    #     pol = []
    #
    #     assessment = (evaluation.diagnosis and
    #         evaluation.diagnosis.rec_name) or ''
    #
    #     # Summarize the encounter note taking as SOAP
    #     soap = \
    #         "S: " + evaluation.chief_complaint + "\n--\n" + \
    #                 evaluation.present_illness +"\n" + \
    #         "O: " + evaluation.evaluation_summary + "\n" + \
    #         "A: " + assessment + "\n" + \
    #         "P: " + evaluation.directions
    #
    #     vals = {
    #         'page': str(uuid4()),
    #         'person': evaluation.patient.name.id,
    #         'page_date': evaluation.evaluation_start,
    #         'age': evaluation.computed_age,
    #         'federation_account': evaluation.patient.name.federation_account,
    #         'page_type':'medical',
    #         'medical_context':'encounter',
    #         'relevance':'important',
    #         'summary': evaluation.chief_complaint,
    #         'info': soap,
    #         'author': evaluation.healthprof.name.rec_name,
    #         'author_acct': evaluation.healthprof.name.federation_account,
    #         'node': evaluation.institution.name.name,
    #         }
    #     if (evaluation.diagnosis):
    #         vals['health_condition_text'] = evaluation.diagnosis.rec_name
    #         vals['health_condition_code'] = evaluation.diagnosis.code
    #
    #     pol.append(vals)
    #     Pol.create(pol)

    # Search by the health condition code or the description
    @api.model
    def search_rec_name(self, name, clause):
        if clause[1].startswith('!') or clause[1].startswith('not '):
            bool_op = 'AND'
        else:
            bool_op = 'OR'
        return [bool_op,
            ('patient',) + tuple(clause[1:]),
            ('code',) + tuple(clause[1:]),
            ]


# SECONDARY CONDITIONS ASSOCIATED TO THE PATIENT IN THE EVALUATION
class SecondaryCondition(models.Model):
    _description ='Secondary Conditions'
    _name = 'medical.secondary_condition'

    evaluation = fields.Many2one(
        'medical.patient.evaluation', 'Evaluation', readonly=True)

    pathology = fields.Many2one(
        'medical.pathology', 'Pathology', required=True)

    comments = fields.Char('Comments')


# PATIENT EVALUATION OTHER DIAGNOSTIC HYPOTHESES
class DiagnosticHypothesis(models.Model):
    _description ='Other Diagnostic Hypothesis'
    _name = 'medical.diagnostic_hypothesis'

    evaluation = fields.Many2one(
        'medical.patient.evaluation', 'Evaluation', readonly=True)

    pathology = fields.Many2one(
        'medical.pathology', 'Pathology', required=True)

    comments = fields.Char('Comments')


# PATIENT EVALUATION CLINICAL FINDINGS (SIGNS AND SYMPTOMS)
class SignsAndSymptoms(models.Model):
    _name = 'medical.signs_and_symptoms'
    _description ='Evaluation Signs and Symptoms'

    evaluation = fields.Many2one(
        'medical.patient.evaluation', 'Evaluation', readonly=True)

    sign_or_symptom = fields.Selection([

        ('sign', 'Sign'),
        ('symptom', 'Symptom')],
        'Subjective / Objective', required=True)

    clinical = fields.Many2one(
        'medical.pathology', 'Sign or Symptom',
        required=True)

    comments = fields.Char('Comments')


# PATIENT EVALUATION DIRECTIONS
class Directions(models.Model):
    _description ='Patient Directions'
    _name = 'medical.directions'

    name = fields.Many2one(
        'medical.patient.evaluation', 'Evaluation', readonly=True)

    # procedure = fields.Many2one(
    #     'gnuhealth.procedure', 'Procedure', required=True)

    comments = fields.Char('Comments')









