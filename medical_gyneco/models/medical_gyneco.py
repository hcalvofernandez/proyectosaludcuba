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
import datetime
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date


class PatientPregnancy(models.Model):
    _name = 'medical.patient.pregnancy'
    _description = 'Patient Pregnancy'

    name = fields.Many2one(
        'medical.patient',
        'Patient',
        domain=[
            ('gender', '=', 'female')
        ]
    )
    gravida = fields.Integer(
        string='Pregnancy #',
        required=True
    )
    computed_age = fields.Char(
        string='Age',
        help='Computed patient age at the moment of LMP',
        compute='patient_age_at_pregnancy'
    )
    warning = fields.Boolean(
        string='Warn',
        help='Check this box if this is pregancy is or was NOT normal'
    )
    warning_icon = fields.Char(
        string='Pregnancy warning icon',
        compute='get_warn_icon'
    )
    reverse = fields.Boolean(
        string='Reverse',
        help="Use this method *only* when the \
        pregnancy information is referred by the patient, as a history taking \
        procedure. Please keep in mind that the reverse pregnancy data is \
        subjective"
    )
    reverse_weeks = fields.Integer(
        string="Pr. Weeks",
        help="Number of weeks at \
        the end of pregnancy. Used only with the reverse input method."
    )
    lmp = fields.Date(
        string='LMP',
        help="Last Menstrual Period",
        required=True
    )
    pdd = fields.Date(
        string='Pregnancy Due Date',
        compute='get_pregnancy_data'
    )
    prenatal_evaluations = fields.One2many(
        comodel_name='medical.patient.prenatal.evaluation',
        inverse_name='name',
        string='Prenatal Evaluations'
    )
    perinatal = fields.One2many(
        comodel_name='medical.perinatal',
        inverse_name='name',
        string='Perinatal Info'
    )
    puerperium_monitor = fields.One2many(
        comodel_name='medical.puerperium.monitor',
        inverse_name='name',
        string='Puerperium Monitor'
    )
    current_pregnancy = fields.Boolean(
        string='Current Pregnancy',
        help='This field marks the current pregnancy'
    )
    fetuses = fields.Integer(
        string='Fetuses',
        required=True
    )
    monozygotic = fields.Boolean(
        string='Monozygotic'
    )
    pregnancy_end_result = fields.Selection(
        [
            ('', ''),
            ('live_birth', 'Live birth'),
            ('abortion', 'Abortion'),
            ('stillbirth', 'Stillbirth'),
            ('status_unknown', 'Status unknown'),
        ],
        string='Result',
        sort=False
    )
    pregnancy_end_date = fields.Datetime(
        string='End of Pregnancy'
    )
    bba = fields.Boolean(
        string='BBA',
        help="Born Before Arrival"
    )
    home_birth = fields.Boolean(
        string='Home Birth',
        help="Home Birth"
    )
    pregnancy_end_age = fields.Integer(
        string='Weeks',
        help='Weeks at the end of pregnancy',
        compute='get_pregnancy_data'
    )
    iugr = fields.Selection(
        [
            ('', ''),
            ('symmetric', 'Symmetric'),
            ('assymetric', 'Asymmetric'),
        ],
        string='IUGR',
        sort=False
    )
    institution = fields.Many2one(
        comodel_name='res.partner',
        string='Institution',
        domain=[
            ('is_institution', '=', True)
        ]
    )
    # TODO: Doctor Relation
    # healthprof = fields.Many2one(
    #     comodel_name='medical.healthprofessional',
    #     string='Health Prof',
    #     readonly=True,
    #     help="Health Professional who created this initial obstetric record"
    # )
    gravidae = fields.Integer(
        string='Pregnancies',
        help="Number of pregnancies, computed from Obstetric history",
        compute='patient_obstetric_info'
    )
    premature = fields.Integer(
        string='Premature',
        help="Preterm < 37 wks live births",
        compute='patient_obstetric_info'
    )
    abortions = fields.Integer(
        string='Abortions',
        compute='patient_obstetric_info'
    )
    stillbirths = fields.Integer(
        string='Stillbirths',
        compute='patient_obstetric_info'
    )
    blood_type = fields.Selection(
        [
            ('', ''),
            ('A', 'A'),
            ('B', 'B'),
            ('AB', 'AB'),
            ('O', 'O'),
        ],
        string='Blood Type',
        sort=False,
        compute='patient_blood_info'
    )
    rh = fields.Selection(
        [
            ('', ''),
            ('+', '+'),
            ('-', '-'),
        ],
        string='Rh',
        compute='patient_blood_info'
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
        computed='patient_blood_info'
    )

    def patient_obstetric_info(self):
        self.gravidae = self.name.gravida
        self.premature = self.name.premature
        self.abortions = self.name.abortions
        self.stillbirths = self.name.stillbirths

    def patient_blood_info(self):
        self.blood_type = self.name.blood_type
        self.rh = self.name.rh
        self.hb = self.name.hb

    @api.depends('name')
    def on_change_name(self):
        self.gravidae = self.name.gravida
        self.premature = self.name.premature
        self.abortions = self.name.abortions
        self.stillbirths = self.name.stillbirths
        self.blood_type = self.name.blood_type
        self.rh = self.name.rh
        self.hb = self.name.hb
    # @classmethod
    # def __setup__(self):
    #     super(PatientPregnancy, self).__setup__()
    #     t = self.__table__()
    #     self._sql_constraints += [
    #         ('gravida_uniq', Unique(t, t.name, t.gravida),
    #             'This pregnancy code for this patient already exists'),
    #     ]
    #     self._order.insert(0, ('lmp', 'DESC'))
    #     self._error_messages.update({
    #         'patient_already_pregnant': 'Our records indicate that the patient'
    #         ' is already pregnant !'})
    # @classmethod
    # def validate(self, pregnancies):
    #     super(PatientPregnancy, self).validate(pregnancies)
    #     for pregnancy in pregnancies:
    #         pregnancy.check_patient_current_pregnancy()
    # def check_patient_current_pregnancy(self):
    #     ''' Check for only one current pregnancy in the patient '''
    #     pregnancy = Table('gnuhealth_patient_pregnancy')
    #     cursor = Transaction().connection.cursor()
    #     patient_id = int(self.name.id)
    #     cursor.execute(*pregnancy.select(Count(pregnancy.name),
    #                                      where=(pregnancy.current_pregnancy == 'true') &
    #                                      (pregnancy.name == patient_id)))
    #     records = cursor.fetchone()[0]
    #     if records > 1:
    #         self.raise_user_error('patient_already_pregnant')

    @api.model
    def default_current_pregnancy():
        return True

    @api.model
    def default_institution(self):
        HealthInst = self.env['res.partner']
        institution = HealthInst.get_institution()
        return institution
    # @staticmethod
    # def default_healthprof():
    #     pool = Pool()
    #     HealthProf = pool.get('medical.healthprofessional')
    #     return HealthProf.get_health_professional()

    @api.depends('reverse_weeks', 'pregnancy_end_date')
    def on_change_with_lmp(self):
        if (self.reverse_weeks and self.pregnancy_end_date):
            estimated_lmp = datetime.date(
                self.pregnancy_end_date - timedelta(self.reverse_weeks*7))
            return estimated_lmp

    def patient_age_at_pregnancy(self):
        for rec in self:
            if (rec.name.birthdate_date and rec.lmp):
                rdelta = relativedelta(
                    rec.lmp,
                    rec.name.birthdate_date
                )
                rec.computed_age = str(rdelta.years)

    def get_pregnancy_data(self):
        for rec in self:
            rec.pdd = self.lmp + timedelta(days=280)
            if rec.pregnancy_end_date:
                gestational_age = datetime.date(
                    self.pregnancy_end_date) - self.lmp
                rec.pregnancy_end_age = int((gestational_age.days) / 7)
            else:
                rec.pregnancy_end_age = 0

    def get_warn_icon(self):
        for rec in self:
            rec.warning_icon = 'medical-normal'
            if rec.warning:
                rec.warning_icon = 'medical-warning'


class PrenatalEvaluation(models.Model):
    _description = 'Prenatal and Antenatal Evaluations'
    _name = 'medical.patient.prenatal.evaluation'

    name = fields.Many2one(
        comodel_name='medical.patient.pregnancy',
        string='Patient Pregnancy'
    )
    evaluation = fields.Many2one(
        comodel_name='medical.patient.evaluation',
        string='Patient Evaluation',
        readonly=True
    )
    evaluation_date = fields.Datetime(
        string='Date',
        required=True
    )
    gestational_weeks = fields.Integer(
        string='Gestational Weeks',
        compute='get_patient_evaluation_data'
    )
    gestational_days = fields.Integer(
        string='Gestational days',
        compute='get_patient_evaluation_data'
    )
    hypertension = fields.Boolean(
        string='Hypertension',
        help='Check this box if the mother has hypertension'
    )
    preeclampsia = fields.Boolean(
        string='Preeclampsia',
        help='Check this box if the mother has pre-eclampsia'
    )
    overweight = fields.Boolean(
        string='Overweight',
        help='Check this box if the mother is overweight or obesity'
    )
    diabetes = fields.Boolean(
        string='Diabetes',
        help='Check this box if the mother has glucose intolerance or diabetes'
    )
    invasive_placentation = fields.Selection(
        [
            ('', ''),
            ('normal', 'Normal decidua'),
            ('accreta', 'Accreta'),
            ('increta', 'Increta'),
            ('percreta', 'Percreta'),
        ],
        string='Placentation',
        sort=False
    )
    placenta_previa = fields.Boolean(
        string='Placenta Previa'
    )
    vasa_previa = fields.Boolean(
        string='Vasa Previa'
    )
    fundal_height = fields.Integer(
        string='Fundal Height',
        help="Distance between the symphysis pubis and the uterine fundus (S-FD) in cm"
    )
    fetus_heart_rate = fields.Integer(
        string='Fetus heart rate',
        help='Fetus heart rate'
    )
    efw = fields.Integer(
        string='EFW',
        help="Estimated Fetal Weight"
    )
    fetal_bpd = fields.Integer(
        string='BPD',
        help="Fetal Biparietal Diameter"
    )
    fetal_ac = fields.Integer(
        string='AC',
        help="Fetal Abdominal Circumference"
    )
    fetal_hc = fields.Integer(
        string='HC',
        help="Fetal Head Circumference"
    )
    fetal_fl = fields.Integer(
        string='FL',
        help="Fetal Femur Length"
    )
    oligohydramnios = fields.Boolean(
        string='Oligohydramnios'
    )
    polihydramnios = fields.Boolean(
        string='Polihydramnios'
    )
    iugr = fields.Boolean(
        string='IUGR',
        help="Intra Uterine Growth Restriction"
    )
    urinary_activity_signs = fields.Boolean(
        string="SUA",
        help="Signs of Urinary System Activity"
    )
    digestive_activity_signs = fields.Boolean(
        string="SDA",
        help="Signs of Digestive Systen Activity"
    )
    notes = fields.Text(
        string="Notes"
    )
    institution = fields.Many2one(
        comodel_name='res.partner',
        string='Institution',
        domain=[
            ('is_institution', '=', True)
        ]
    )
    # healthprof = fields.Many2one(
    #     comodel_name='medical.healthprofessional',
    #     string='Health Prof',
    #     readonly=True,
    #     help="Health Professional in charge, or that who entered the information in the system"
    # )

    @api.model
    def default_institution(self):
        HealthInst = self.env['res.partner']
        institution = HealthInst.get_institution()
        return institution
    # @staticmethod
    # def default_healthprof():
    #     pool = Pool()
    #     HealthProf = pool.get('medical.healthprofessional')
    #     return HealthProf.get_health_professional()

    def get_patient_evaluation_data(self):
        gestational_age = datetime.datetime.date(
            self.evaluation_date) - self.name.lmp
        self.gestational_weeks = (gestational_age.days) / 7
        gestational_age = datetime.datetime.date(
            self.evaluation_date) - self.name.lmp
        self.gestational_days = gestational_age.days

    @api.model
    def default_get(self, fields):
        res = super(PrenatalEvaluation, self).default_get(fields)
        res.update(
            {
                'evaluation_date': datetime.now()
            }
        )
        return res


class PuerperiumMonitor(models.Model):
    _name = 'medical.puerperium.monitor'
    _description = 'Puerperium Monitor'

    name = fields.Many2one(
        comodel_name='medical.patient.pregnancy',
        string='Patient Pregnancy'
    )
    date = fields.Datetime(
        string='Date and Time',
        required=True
    )
    systolic = fields.Integer(
        string='Systolic Pressure'
    )
    diastolic = fields.Integer(
        string='Diastolic Pressure'
    )
    frequency = fields.Integer(
        string='Heart Frequency'
    )
    temperature = fields.Float(
        string='Temperature'
    )
    lochia_amount = fields.Selection(
        [
            ('', ''),
            ('n', 'normal'),
            ('e', 'abundant'),
            ('h', 'hemorrhage'),
        ],
        string='Lochia amount',
        sort=False
    )
    lochia_color = fields.Selection(
        [
            ('', ''),
            ('r', 'rubra'),
            ('s', 'serosa'),
            ('a', 'alba'),
        ],
        string='Lochia color',
        sort=False
    )
    lochia_odor = fields.Selection(
        [
            ('', ''),
            ('n', 'normal'),
            ('o', 'offensive'),
        ],
        string='Lochia odor',
        sort=False
    )
    uterus_involution = fields.Integer(
        string='Fundal Height',
        help="Distance between the symphysis pubis and the uterine fundus (S-FD) in cm"
    )
    institution = fields.Many2one(
        comodel_name='res.partner',
        string='Institution',
        domain=[
            ('is_institution', '=', True)
        ]
    )
    # healthprof = fields.Many2one(
    #     comodel_name='medical.healthprofessional',
    #     string='Health Prof',
    #     readonly=True,
    #     help="Health Professional in charge, or that who entered the information in the system"
    # )

    @api.model
    def default_institution(self):
        HealthInst = self.env['res.partner']
        institution = HealthInst.get_institution()
        return institution
    # @staticmethod
    # def default_healthprof():
    #     pool = Pool()
    #     HealthProf = pool.get('medical.healthprofessional')
    #     return HealthProf.get_health_professional()

    @api.model
    def default_get(self, fields):
        res = super(PuerperiumMonitor, self).default_get(fields)
        res.update(
            {
                'date': datetime.now()
            }
        )
        return res


class Perinatal(models.Model):
    _name = 'medical.perinatal'
    _description = 'Perinatal Information'

    name = fields.Many2one(
        comodel_name='medical.patient.pregnancy',
        string='Patient Pregnancy'
    )
    admission_code = fields.Char(
        string='Code'
    )
    gravida_number = fields.Integer(
        string='Gravida #'
    )
    abortion = fields.Boolean(
        string='Abortion'
    )
    stillbirth = fields.Boolean(
        string='Stillbirth'
    )
    admission_date = fields.Datetime(
        string='Admission',
        help="Date when she was admitted to give birth",
        required=True
    )
    prenatal_evaluations = fields.Integer(
        string='Prenatal evaluations',
        help="Number of visits to the doctor during pregnancy"
    )
    start_labor_mode = fields.Selection(
        [
            ('', ''),
            ('v', 'Vaginal - Spontaneous'),
            ('ve', 'Vaginal - Vacuum Extraction'),
            ('vf', 'Vaginal - Forceps Extraction'),
            ('c', 'C-section'),
        ],
        string='Delivery mode',
        sort=False
    )
    gestational_weeks = fields.Integer(
        string='Gestational wks',
        compute='get_perinatal_information'
    )
    gestational_days = fields.Integer(
        string='Days'
    )
    fetus_presentation = fields.Selection(
        [
            ('', ''),
            ('cephalic', 'Cephalic'),
            ('breech', 'Breech'),
            ('shoulder', 'Shoulder'),
        ],
        string='Fetus Presentation',
        sort=False
    )
    dystocia = fields.Boolean(
        string='Dystocia'
    )
    placenta_incomplete = fields.Boolean(
        string='Incomplete',
        help='Incomplete Placenta'
    )
    placenta_retained = fields.Boolean(
        string='Retained',
        help='Retained Placenta'
    )
    abruptio_placentae = fields.Boolean(
        string='Abruptio Placentae',
        help='Abruptio Placentae'
    )
    episiotomy = fields.Boolean(
        string='Episiotomy'
    )
    vaginal_tearing = fields.Boolean(
        string='Vaginal tearing'
    )
    forceps = fields.Boolean(
        string='Forceps'
    )
    monitoring = fields.One2many(
        comodel_name='medical.perinatal.monitor',
        inverse_name='name',
        string='Monitors'
    )
    laceration = fields.Selection(
        [
            ('', ''),
            ('perineal', 'Perineal'),
            ('vaginal', 'Vaginal'),
            ('cervical', 'Cervical'),
            ('broad_ligament', 'Broad Ligament'),
            ('vulvar', 'Vulvar'),
            ('rectal', 'Rectal'),
            ('bladder', 'Bladder'),
            ('urethral', 'Urethral'),
        ],
        string='Lacerations',
        sort=False
    )
    hematoma = fields.Selection(
        [
            ('', ''),
            ('vaginal', 'Vaginal'),
            ('vulvar', 'Vulvar'),
            ('retroperitoneal', 'Retroperitoneal'),
        ],
        string='Hematoma',
        sort=False
    )
    notes = fields.Text(
        string='Notes'
    )
    institution = fields.Many2one(
        comodel_name='res.partner',
        string='Institution',
        domain=[
            ('is_institution', '=', True)
        ]
    )
    # healthprof = fields.Many2one(
    #     'medical.healthprofessional', 'Health Prof', readonly=True,
    #     help="Health Professional in charge, or that who entered the \
    #         information in the system")

    @api.model
    def default_institution(self):
        HealthInst = self.env['res.partner']
        institution = HealthInst.get_institution()
        return institution
    # @staticmethod
    # def default_healthprof():
    #     pool = Pool()
    #     HealthProf = pool.get('medical.healthprofessional')
    #     return HealthProf.get_health_professional()

    @api.model
    def default_get(self, fields):
        res = super(Perinatal, self).default_get(fields)
        res.update(
            {
                'admission_date': datetime.now()
            }
        )
        return res

    def get_perinatal_information(self):
        gestational_age = datetime.datetime.date(
            self.admission_date) - self.name.lmp
        self.gestational_weeks = (gestational_age.days) / 7


class PerinatalMonitor(models.Model):
    _name = 'medical.perinatal.monitor'
    _description = 'Perinatal Monitor'

    name = fields.Many2one(
        comodel_name='medical.perinatal',
        string='Patient Perinatal Evaluation'
    )
    date = fields.Datetime(
        string='Date and Time'
    )
    systolic = fields.Integer(
        string='Systolic Pressure'
    )
    diastolic = fields.Integer(
        string='Diastolic Pressure'
    )
    contractions = fields.Integer(
        string='Contractions'
    )
    frequency = fields.Integer(
        string='Mother\'s Heart Frequency'
    )
    dilation = fields.Integer(
        string='Cervix dilation'
    )
    f_frequency = fields.Integer(
        string='Fetus Heart Frequency'
    )
    meconium = fields.Boolean(
        string='Meconium'
    )
    bleeding = fields.Boolean(
        string='Bleeding'
    )
    fundal_height = fields.Integer(
        string='Fundal Height'
    )
    fetus_position = fields.Selection(
        [
            ('', ''),
            ('o', 'Occiput / Cephalic Posterior'),
            ('fb', 'Frank Breech'),
            ('cb', 'Complete Breech'),
            ('t', 'Transverse Lie'),
            ('t', 'Footling Breech'),
        ],
        string='Fetus Position',
        sort=False
    )

    @api.model
    def default_get(self, fields):
        res = super(PerinatalMonitor, self).default_get(fields)
        res.update(
            {
                'date': datetime.now()
            }
        )
        return res


class MedicalPatient(models.Model):
    _inherit = 'medical.patient'
    _description = 'Add to the Medical patient_data class (medical.patient) the gynecological and obstetric fields.'

    currently_pregnant = fields.Boolean(
        string='Pregnant',
        compute='get_pregnancy_info'
    )
    fertile = fields.Boolean(
        string='Fertile',
        help="Check if patient is in fertile age"
    )
    menarche = fields.Integer(
        string='Menarche age'
    )
    menopausal = fields.Boolean(
        string='Menopausal'
    )
    menopause = fields.Integer(
        string='Menopause age'
    )
    mammography = fields.Boolean(
        string='Mammography',
        help="Check if the patient does periodic mammographys"
    )
    mammography_last = fields.Date(
        string='Last mammography',
        help="Enter the date of the last mammography"
    )
    breast_self_examination = fields.Boolean(
        string='Breast self-examination',
        help="Check if patient does and knows how to self examine her breasts"
    )
    pap_test = fields.Boolean(
        string='PAP test',
        help="Check if patient does periodic cytologic pelvic smear screening"
    )
    pap_test_last = fields.Date(
        string='Last PAP test',
        help="Enter the date of the last Papanicolau test"
    )
    colposcopy = fields.Boolean(
        string='Colposcopy',
        help="Check if the patient has done a colposcopy exam"
    )
    colposcopy_last = fields.Date(
        string='Last colposcopy',
        help="Enter the date of the last colposcopy"
    )
    gravida = fields.Integer(
        string='Pregnancies',
        help="Number of pregnancies, computed from Obstetric history",
        compute='patient_obstetric_info'
    )
    premature = fields.Integer(
        string='Premature',
        help="Preterm < 37 wks live births",
        compute='patient_obstetric_info'
    )
    abortions = fields.Integer(
        string='Abortions',
        compute='patient_obstetric_info'
    )
    stillbirths = fields.Integer(
        string='Stillbirths',
        compute='patient_obstetric_info'
    )
    full_term = fields.Integer(
        string='Full Term',
        help="Full term pregnancies"
    )
    gpa = fields.Char(
        string='GPA',
        help="Gravida, Para, Abortus Notation. For example G4P3A1 : 4 Pregnancies, 3 viable and 1 abortion"
    )
    born_alive = fields.Integer(
        string='Born Alive'
    )
    deaths_1st_week = fields.Integer(
        string='Deceased during 1st week',
        help="Number of babies that die in the first week"
    )
    deaths_2nd_week = fields.Integer(
        string='Deceased after 2nd week',
        help="Number of babies that die after the second week"
    )
    perinatal = fields.One2many(
        comodel_name='medical.perinatal',
        inverse_name='name',
        string='Perinatal Info'
    )
    menstrual_history = fields.One2many(
        comodel_name='medical.patient.menstrual_history',
        inverse_name='name',
        string='Menstrual History'
    )
    mammography_history = fields.One2many(
        comodel_name='medical.patient.mammography_history',
        inverse_name='name',
        string='Mammography History'
    )
    pap_history = fields.One2many(
        comodel_name='medical.patient.pap_history',
        inverse_name='name',
        string='PAP smear History'
    )
    colposcopy_history = fields.One2many(
        comodel_name='medical.patient.colposcopy_history',
        inverse_name='name',
        string='Colposcopy History'
    )
    pregnancy_history = fields.One2many(
        comodel_name='medical.patient.pregnancy',
        inverse_name='name',
        string='Pregnancies'
    )

    def get_pregnancy_info(self):
        self.currently_pregnant = False
        for pregnancy_history in self.pregnancy_history:
            if pregnancy_history.current_pregnancy:
                self.currently_pregnant = True

    def patient_obstetric_info(self):
        ''' Return the number of pregnancies, perterm,
        abortion and stillbirths '''
        counter = 0
        pregnancies = len(self.pregnancy_history)
        self.gravida = pregnancies
        prematures = 0
        while counter < pregnancies:
            result = self.pregnancy_history[counter].pregnancy_end_result
            preg_weeks = self.pregnancy_history[counter].pregnancy_end_age
            if (result == "live_birth" and
                    preg_weeks < 37):
                prematures = prematures+1
            counter = counter+1
        self.premature = prematures
        abortions = 0
        while counter < pregnancies:
            result = self.pregnancy_history[counter].pregnancy_end_result
            preg_weeks = self.pregnancy_history[counter].pregnancy_end_age
            if (result == "abortion"):
                abortions = abortions+1
            counter = counter+1
        self.abortions = abortions
        stillbirths = 0
        while counter < pregnancies:
            result = self.pregnancy_history[counter].pregnancy_end_result
            preg_weeks = self.pregnancy_history[counter].pregnancy_end_age
            if (result == "stillbirth"):
                stillbirths = stillbirths+1
            counter = counter+1
        self.stillbirths = stillbirths


class PatientMenstrualHistory(models.Model):
    _name = 'medical.patient.menstrual_history'
    _description = 'Menstrual History'

    name = fields.Many2one(
        comodel_name='medical.patient',
        string='Patient',
        readonly=True,
        required=True
    )
    evaluation = fields.Many2one(
        comodel_name='medical.patient.evaluation',
        string='Evaluation',
        domain=[
            ('patient', '=', 'name')
        ],
        depends=['name']
    )
    evaluation_date = fields.Date(
        string='Date',
        help="Evaluation Date",
        required=True
    )
    lmp = fields.Date(
        string='LMP',
        help="Last Menstrual Period",
        required=True
    )
    lmp_length = fields.Integer(
        string='Length',
        required=True
    )
    is_regular = fields.Boolean(
        string='Regular'
    )
    dysmenorrhea = fields.Boolean(
        string='Dysmenorrhea'
    )
    frequency = fields.Selection(
        [
            ('amenorrhea', 'amenorrhea'),
            ('oligomenorrhea', 'oligomenorrhea'),
            ('eumenorrhea', 'eumenorrhea'),
            ('polymenorrhea', 'polymenorrhea'),
        ],
        string='frequency',
        sort=False
    )
    volume = fields.Selection(
        [
            ('hypomenorrhea', 'hypomenorrhea'),
            ('normal', 'normal'),
            ('menorrhagia', 'menorrhagia'),
        ],
        string='volume',
        sort=False
    )
    institution = fields.Many2one(
        comodel_name='res.partner',
        string='Institution',
        domain=[
            ('is_institution', '=', True)
        ]
    )
    # healthprof = fields.Many2one(
    #     'medical.healthprofessional', 'Reviewed', readonly=True,
    #     help="Health Professional who reviewed the information")

    @api.model
    def default_institution(self):
        HealthInst = self.env['res.partner']
        institution = HealthInst.get_institution()
        return institution
    # @staticmethod
    # def default_healthprof():
    #     pool = Pool()
    #     HealthProf = pool.get('medical.healthprofessional')
    #     return HealthProf.get_health_professional()

    @api.model
    def default_get(self, fields):
        res = super(PatientMenstrualHistory, self).default_get(fields)
        res.update(
            {
                'evaluation_date': datetime.now()
            }
        )
        return res

    @api.model
    def default_frequency():
        return 'eumenorrhea'

    @api.model
    def default_volume():
        return 'normal'


class PatientMammographyHistory(models.Model):
    _name = 'medical.patient.mammography_history'
    _description = 'Mammography History'

    name = fields.Many2one(
        comodel_name='medical.patient',
        string='Patient',
        readonly=True,
        required=True
    )
    evaluation = fields.Many2one(
        comodel_name='medical.patient.evaluation',
        string='Evaluation',
        domain=[
            ('patient', '=', 'name')
        ],
        depends=['name']
    )
    evaluation_date = fields.Date(
        string='Date',
        help="Date",
        required=True
    )
    last_mammography = fields.Date(
        string='Previous',
        help="Last Mammography"
    )
    result = fields.Selection(
        [
            ('', ''),
            ('normal', 'normal'),
            ('abnormal', 'abnormal'),
        ],
        string='result',
        help="Please check the lab test results if the module is installed",
        sort=False
    )
    comments = fields.Char(
        string='Remarks'
    )
    institution = fields.Many2one(
        comodel_name='res.partner',
        string='Institution',
        domain=[
            ('is_institution', '=', True)
        ]
    )
    # healthprof = fields.Many2one(
    #     'medical.healthprofessional', 'Reviewed', readonly=True,
    #     help="Health Professional who last reviewed the test")

    @api.model
    def default_institution(self):
        HealthInst = self.env['res.partner']
        institution = HealthInst.get_institution()
        return institution
    # @staticmethod
    # def default_healthprof():
    #     pool = Pool()
    #     HealthProf = pool.get('medical.healthprofessional')
    #     return HealthProf.get_health_professional()

    @api.model
    def default_get(self, fields):
        res = super(PatientMammographyHistory, self).default_get(fields)
        res.update(
            {
                'evaluation_date': datetime.now(),
                'last_mammography': datetime.now()
            }
        )
        return res


class PatientPAPHistory(models.Model):
    _name = 'medical.patient.pap_history'
    _description = 'PAP Test History'

    name = fields.Many2one(
        comodel_name='medical.patient',
        string='Patient',
        readonly=True,
        required=True
    )
    evaluation = fields.Many2one(
        comodel_name='medical.patient.evaluation',
        string='Evaluation',
        domain=[
            ('patient', '=', 'name')
        ],
        depends=['name']
    )
    evaluation_date = fields.Date(
        string='Date',
        help="Date",
        required=True
    )
    last_pap = fields.Date(
        string='Previous',
        help="Last Papanicolau"
    )
    result = fields.Selection(
        [
            ('', ''),
            ('negative', 'Negative'),
            ('c1', 'ASC-US'),
            ('c2', 'ASC-H'),
            ('g1', 'ASG'),
            ('c3', 'LSIL'),
            ('c4', 'HSIL'),
            ('g4', 'AIS'),
        ],
        string='result',
        help="Please check the lab results if the module is installed",
        sort=False
    )
    comments = fields.Char(
        string='Remarks'
    )
    institution = fields.Many2one(
        comodel_name='res.partner',
        string='Institution',
        domain=[
            ('is_institution', '=', True)
        ]
    )
    # healthprof = fields.Many2one(
    #     'gnuhealth.healthprofessional', 'Reviewed', readonly=True,
    #     help="Health Professional who last reviewed the test")

    @api.model
    def default_institution(self):
        HealthInst = self.env['res.partner']
        institution = HealthInst.get_institution()
        return institution
    # @staticmethod
    # def default_healthprof():
    #     pool = Pool()
    #     HealthProf = pool.get('gnuhealth.healthprofessional')
    #     return HealthProf.get_health_professional()

    @api.model
    def default_get(self, fields):
        res = super(PatientPAPHistory, self).default_get(fields)
        res.update(
            {
                'evaluation_date': datetime.now(),
                'last_pap': datetime.now()
            }
        )
        return res


class PatientColposcopyHistory(models.Model):
    _name = 'medical.patient.colposcopy_history'
    _description = 'Colposcopy History'

    name = fields.Many2one(
        comodel_name='medical.patient',
        string='Patient',
        readonly=True,
        required=True
    )
    evaluation = fields.Many2one(
        comodel_name='medical.patient.evaluation',
        string='Evaluation',
        domain=[
            ('patient', '=', 'name')
        ],
        depends=['name']
    )
    evaluation_date = fields.Date(
        string='Date',
        help="Date",
        required=True
    )
    last_colposcopy = fields.Date(
        string='Previous',
        help="Last colposcopy"
    )
    result = fields.Selection(
        [
            ('', ''),
            ('normal', 'normal'),
            ('abnormal', 'abnormal'),
        ],
        string='result',
        help="Please check the lab test results if the module is installed",
        sort=False
    )
    comments = fields.Char(
        string='Remarks'
    )
    institution = fields.Many2one(
        comodel_name='res.partner',
        string='Institution',
        domain=[
            ('is_institution', '=', True)
        ]
    )
    # healthprof = fields.Many2one(
    #     'gnuhealth.healthprofessional', 'Reviewed', readonly=True,
    #     help="Health Professional who last reviewed the test")

    @api.model
    def default_institution(self):
        HealthInst = self.env['res.partner']
        institution = HealthInst.get_institution()
        return institution
    # @staticmethod
    # def default_healthprof():
    #     pool = Pool()
    #     HealthProf = pool.get('gnuhealth.healthprofessional')
    #     return HealthProf.get_health_professional()

    @api.model
    def default_get(self, fields):
        res = super(PatientColposcopyHistory, self).default_get(fields)
        res.update(
            {
                'evaluation_date': datetime.now(),
                'last_colposcopy': datetime.now()
            }
        )
        return res
