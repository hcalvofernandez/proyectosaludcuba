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
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.osv import expression

import pytz

__all__ = ['DietTherapeutic', 'InpatientRegistration',
           'BedTransfer', 'Appointment', 'PatientEvaluation', 'MedicalPatient',
           'InpatientMedication', 'InpatientMedicationAdminTimes',
           'InpatientMedicationLog', 'InpatientDiet', 'InpatientMeal',
           'InpatientMealOrder', 'InpatientMealOrderItem', 'PatientECG']


# Therapeutic Diet types

class DietTherapeutic(models.Model):
    _description = 'Diet Therapy'
    _name = "medical.diet.therapeutic"

    name = fields.Char(
        'Diet type',
        required=True,
        translate=True
    )
    code = fields.Char(
        'Code',
        required=True
    )
    description = fields.Text(
        'Indications',
        required=True,
        translate=True
    )

    _sql_constraints = [
        ('code_uniq', 'unique (code)', 'The Diet code already exists!'),
    ]


class InpatientRegistration(models.Model):
    _description = 'Patient admission History'
    _name = 'medical.inpatient.registration'

    @api.model
    def _get_default_institution(self):
        HealthInst = self.env['res.partner']
        institution = HealthInst.get_institution()
        return institution

    name = fields.Char(
        'Registration Code',
        readonly=True,
        index=True
    )
    patient = fields.Many2one(
        'medical.patient',
        'Patient',
        required=True,
        index=True,
        readonly=True,
        states={
            'done': [('readonly', True)],
            'finished': [('readonly', True)],
        },
    )
    admission_type = fields.Selection(
        [
            ('none', ''),
            ('routine', 'Routine'),
            ('maternity', 'Maternity'),
            ('elective', 'Elective'),
            ('urgent', 'Urgent'),
            ('emergency', 'Emergency'),
        ],
        'Admission type',
        default='none',
        required=True,
        index=True,
        readonly=True,
        states={
            'done': [('readonly', True)],
            'finished': [('readonly', True)],
        },
    )
    hospitalization_date = fields.Datetime(
        'Hospitalization date',
        required=True,
        index=True,
        readonly=True,
        states={
            'done': [('readonly', True)],
            'finished': [('readonly', True)],
        },
    )
    discharge_date = fields.Datetime(
        'Expected Discharge Date',
        required=True,
        readonly=True,
        states={
            'done': [('readonly', True)],
            'finished': [('readonly', True)],
        },
    )
    attending_physician = fields.Many2one(
        'res.partner',
        'Attending Physician',
        domain=[('is_healthprof', '=', True)],
        readonly=True,
        states={
            'done': [('readonly', True)],
            'finished': [('readonly', True)],
        },
    )
    operating_physician = fields.Many2one(
        'res.partner',
        'Operating Physician',
        domain=[('is_healthprof', '=', True)],
        readonly=True,
        states={
            'done': [('readonly', True)],
            'finished': [('readonly', True)],
        },
    )
    admission_reason = fields.Many2one(
        'medical.pathology',
        'Reason for Admission',
        help="Reason for Admission",
        readonly=True,
        states={
            'done': [('readonly', True)],
            'finished': [('readonly', True)],
        },
        index=True
    )
    bed = fields.Many2one(
        'medical.hospital.bed',
        'Hospital Bed',
        readonly=True,
        states={
            'done': [('readonly', True)],
            'finished': [('readonly', True)],
        },
        depends=['name']
    )
    nursing_plan = fields.Text(
        'Nursing Plan',
        readonly=True,
        states={
            'done': [('readonly', True)],
            'finished': [('readonly', True)],
        },
    )
    medications = fields.One2many(
        'medical.inpatient.medication',
        'name',
        'Medications',
        readonly=True,
        states={
            'done': [('readonly', True)],
            'finished': [('readonly', True)],
        },
    )
    therapeutic_diets = fields.One2many(
        'medical.inpatient.diet',
        'name',
        'Meals / Diet Program',
        readonly=True,
        states={
            'done': [('readonly', True)],
            'finished': [('readonly', True)],
        },
    )

    nutrition_notes = fields.Text(
        'Nutrition notes / directions',
        readonly=True,
        states={
            'done': [('readonly', True)],
            'finished': [('readonly', True)],
        },
    )
    discharge_plan = fields.Text(
        'Discharge Plan',
        readonly=True,
        states={
            'done': [('readonly', True)],
            'finished': [('readonly', True)],
        },
    )
    info = fields.Text(
        'Notes',
        readonly=True,
        states={
            'done': [('readonly', True)],
            'finished': [('readonly', True)],
        },
    )
    state = fields.Selection(
        [
            ('none', ''),
            ('free', 'free'),
            ('cancelled', 'cancelled'),
            ('confirmed', 'confirmed'),
            ('hospitalized', 'hospitalized'),
            ('done', 'Discharged - needs cleaning'),
            ('finished', 'Finished'),
        ],
        'Status',
        index=True,
        default='free',
        readonly=True
    )

    bed_transfers = fields.One2many('medical.bed.transfer',
                                    'name',
                                    'Transfer History',
                                    readonly=True)

    discharged_by = fields.Many2one(
        'res.partner',
        'Discharged by',
        domain=[('is_healthprof', '=', True)],
        readonly=True,
        help="Health Professional that discharged the patient"
    )

    discharge_reason = fields.Selection(
        [
            ('none', ''),
            ('home', 'Home / Selfcare'),
            ('transfer', 'Transferred to another institution'),
            ('death', 'Death'),
            ('against_advice', 'Left against medical advice'),
        ],
        'Discharge Reason',
        default='none',
        readonly=True,
        states={
            'hospitalized': [('readonly', False)],
        },
        help="Reason for patient discharge"
    )

    discharge_dx = fields.Many2one(
        'medical.pathology',
        'Discharge Dx',
        help="Code for Discharge Diagnosis",
        readonly=True,
        states={
            'hospitalized': [('readonly', True)],
        },
    )

    institution = fields.Many2one(
        'res.partner',
        'Institution',
        readonly=True,
        default=_get_default_institution
    )

    # puid = fields.Char(
    #     'PUID',
    #     help="Person Unique Identifier",
    #     compute='_get_patient_puid',
    #     search='_search_patient_puid',
    # )

    # @api.depends('patient')
    # def _get_patient_puid(self):
    #     return self.patient.name
    #
    # def search_patient_puid(self, operator, value):
    #     res = []
    #     res.append(('patient.name', operator, value))
    #     return res

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The Registration code already exists!'),
    ]

    ## Method to check for availability and make the hospital bed reservation
    # Checks that there are not overlapping dates and status of the bed / room
    # is not confirmed, hospitalized or done but requiring cleaning ('done')
    def button_confirmed(self):
        self.ensure_one()
        Bed = self.env['medical.hospital.bed']
        cursor = self.env.cr
        bed_id = self.bed.id
        cursor.execute("SELECT COUNT(*) \
            FROM medical_inpatient_registration \
            WHERE (hospitalization_date::timestamp,discharge_date::timestamp) \
                OVERLAPS (timestamp %s, timestamp %s) \
              AND (state = %s or state = %s or state = %s) \
              AND bed = CAST(%s AS INTEGER) ",
                       (self.hospitalization_date,
                        self.discharge_date,
                        'confirmed', 'hospitalized', 'done', str(bed_id)))
        res = cursor.fetchone()
        if self.discharge_date.date() < self.hospitalization_date.date():
            raise UserError(
                _(
                    'The Discharge date must later than the Admission!'
                ))
        if res[0] > 0:
            raise UserError(
                _(
                    'Bed is not available!'
                ))
        else:
            self.write({'state': 'confirmed'})
            self.bed.write({'state': 'reserved'})

    def button_discharge(self):
        self.ensure_one()
        Bed = self.env['medical.hospital.bed']

        signing_hp = self.env['res.partner'].get_health_professional()
        if not signing_hp:
            raise UserError(
                _(
                    'No health professional associated to this user!'
                ))

        self.write({'state': 'done',
                    'discharged_by': signing_hp})

        self.bed.write({'state': 'to_clean'})

    def button_bedclean(self):
        self.ensure_one()
        Bed = self.env['medical.hospital.bed']

        self.write({'state': 'finished'})

        self.bed.write({'state': 'free'})

    def button_cancel(self):
        self.ensure_one()
        Bed = self.env['medical.hospital.bed']

        self.write({'state': 'cancelled'})
        self.bed.write({'state': 'free'})

    def button_admission(self):
        self.ensure_one()
        Bed = self.env['medical.hospital.bed']

        Company = self.env['res.company']

        timezone = None
        company_id = self._context.get('company')
        if company_id:
            company = Company(company_id)
            if company.timezone:
                timezone = pytz.timezone(company.timezone)

                dt = datetime.today()
                dt_local = datetime.astimezone(dt.replace(tzinfo=pytz.utc),
                                               timezone)

                if (self.hospitalization_date.date() !=
                        dt_local.date()):
                    raise UserError(
                        _(
                            'The Admission date must be today.'
                        ))
                else:
                    self.write({'state': 'hospitalized'})
                    self.bed.write({'state': 'occupied'})

            else:
                raise UserError(
                    _(
                        'You need to set up the company timezone.'
                    ))

    @api.model_create_multi
    def create(self, vals_list):
        vals_list = [x.copy() for x in vals_list]
        for values in vals_list:
            if not values.get('name'):
                values['name'] = self.env['ir.sequence'].next_by_code('medical.inpatient.registration')
        return super(InpatientRegistration, self).create(vals_list)

    @api.constrains('admission_reason', 'state', 'discharge_dx')
    def validate(self):
        super(InpatientRegistration, self).validate()
        for registration in self:
            registration.check_discharge_context()

    def check_discharge_context(self):
        if ((not self.discharge_reason or not self.discharge_dx
             or not self.admission_reason)
            and self.state == 'done'):
            raise UserError(
                _(
                    'Admission and Discharge reasons \n'
                    'as well as Discharge Dx are needed.'
                ))

    # Format Registration ID : Patient : Bed
    def _get_name(self):
        if self.patient:
            return self.name + ':' + self.bed.rec_name + ':' + self.patient.rec_name
        else:
            return self.name

    # Allow searching by the hospitalization code, patient name
    # or bed number

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        # Search by Registration Code ID or Patient
        args = args or []
        if operator.startswith('!') or operator.startswith('not '):
            domain = [('name', operator, name),
                      ('patient.name', operator, name),
                      ('bed.name', operator, name)]
        else:
            domain = ['|', '|',
                      ('name', operator, name),
                      ('patient.name', operator, name),
                      ('bed.name', operator, name)]
        rec = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(rec).with_user(name_get_uid))


class BedTransfer(models.Model):
    _description = 'Bed transfers'
    _name = 'medical.bed.transfer'

    name = fields.Many2one(
        'medical.inpatient.registration',
        'Registration Code'
    )
    transfer_date = fields.Datetime(
        'Date'
    )
    bed_from = fields.Many2one(
        'medical.hospital.bed',
        'From',
    )
    bed_to = fields.Many2one(
        'medical.hospital.bed',
        'To',
    )
    reason = fields.Char(
        'Reason'
    )


class Appointment(models.Model):
    _name = 'medical.appointment'
    _inherit = 'medical.appointment'

    inpatient_registration_code = fields.Many2one(
        'medical.inpatient.registration',
        'Inpatient Registration',
        help="Enter the patient hospitalization code"
    )





class MedicalPatient(models.Model):
    """Inherit patient model and add the patient status to the patient."""
    _name = 'medical.patient'
    _inherit = 'medical.patient'

    patient_status = fields.Boolean(
        'Hospitalized',
        help="Show the hospitalization status of the patient",
        compute='_get_patient_status',
        search='_search_patient_status'
    )

    def _get_patient_status(self):
        cursor = self.env.cr
        cursor.execute("SELECT gir.id \
                        FROM medical_inpatient_registration gir \
                        WHERE (gir.state = %s and patient =  %s) \
                        GROUP BY gir.id",
                       ('hospitalized', self.id))
        res = cursor.fetchall()

        if res:
            self.patient_status = True
        else:
            self.patient_status = False

    def _search_patient_status(self, operator, value):

        # Validate operator and value
        if operator not in ['=', '!=']:
            raise ValueError('Wrong operator: %s' % operator)
        if value is not True and value is not False:
            raise ValueError('Wrong value: %s' % value)

        # Find hospitalized patient ids
        cursor = self.env.cr
        bed_id = self.bed.id
        cursor.execute("SELECT pat.id \
            FROM medical_inpatient_registration gir join medical_patient pat on pat.id = gir.patient \
            WHERE (gir.state = %s )",
                       ('hospitalized',))
        query_res = self._cr.fetchall()

        # Choose domain operator
        if (operator == '=' and value) or (operator == '!=' and not value):
            d = 'in'
        else:
            d = 'not in'

        return [('id', d, query_res)]


class InpatientMedication(models.Model):
    _description = 'Inpatient Medication'
    _name = 'medical.inpatient.medication'

    name = fields.Many2one(
        'medical.inpatient.registration',
        'Registration Code'
    )
    medicament = fields.Many2one(
        'medical.medicament',
        'Medicament',
        required=True,
        help='Prescribed Medicament'
    )
    indication = fields.Many2one(
        'medical.pathology',
        'Indication',
        help='Choose a disease for this medicament from the disease list. It'
             ' can be an existing disease of the patient or a prophylactic.'
    )
    start_treatment = fields.Datetime(
        'Start',
        help='Date of start of Treatment',
        required=True
    )
    end_treatment = fields.Datetime(
        'End',
        help='Date of start of Treatment'
    )
    dose = fields.Float(
        'Dose',
        help='Amount of medication (eg, 250 mg) per dose',
        required=True
    )
    dose_unit = fields.Many2one(
        'medical.dose.unit',
        'dose unit',
        required=True,
        help='Unit of measure for the medication to be taken'
    )
    route = fields.Many2one(
        'medical.drug.route',
        'Administration Route',
        required=True,
        help='Drug administration route code.'
    )
    form = fields.Many2one(
        'medical.drug.form',
        'Form',
        required=True,
        help='Drug form, such as tablet or gel'
    )
    qty = fields.Integer(
        'x',
        required=True,
        help='Quantity of units (eg, 2 capsules) of the medicament'
    )
    #TODO falta la clase 'medical.medication.dosage' ???
    # common_dosage = fields.Many2one(
    #     'medical.medication.dosage',
    #     'Frequency',
    #     help='Common / standard dosage frequency for this medicament'
    # )
    admin_times = fields.One2many(
        'medical.inpatient.medication.admin_time',
        'name',
        "Admin times"
    )
    log_history = fields.One2many(
        'medical.inpatient.medication.log',
        'name',
        "Log History"
    )
    frequency = fields.Integer(
        'Frequency',
        help='Time in between doses the patient must wait (ie, for 1 pill'
             ' each 8 hours, put here 8 and select \"hours\" in the unit field'
    )
    frequency_unit = fields.Selection(
        [
            ('none', ''),
            ('seconds', 'seconds'),
            ('minutes', 'minutes'),
            ('hours', 'hours'),
            ('days', 'days'),
            ('weeks', 'weeks'),
            ('wr', 'when required'),
        ],
        'unit',
        index=True,
        sort=False
    )
    frequency_prn = fields.Boolean(
        'PRN',
        help='Use it as needed, pro re nata'
    )
    is_active = fields.Boolean(
        'Active',
        default=True,
        help='Check if the patient is currently taking the medication'
    )
    discontinued = fields.Boolean(
        'Discontinued'
    )
    course_completed = fields.Boolean(
        'Course Completed'
    )
    discontinued_reason = fields.Char(
        'Reason for discontinuation',
        depends=['discontinued'],
        help='Short description for discontinuing the treatment'
    )
    adverse_reaction = fields.Text(
        'Adverse Reactions',
        help='Side effects or adverse reactions that the patient experienced'
    )

    @api.depends('discontinued',
                 'course_completed')
    def on_change_with_is_active(self):
        is_active = True
        if self.discontinued or self.course_completed:
            is_active = False
        return is_active

    @api.depends('is_active',
                 'course_completed')
    def on_change_with_discontinued(self):
        return not (self.is_active or self.course_completed)

    @api.depends('is_active',
                 'discontinued')
    def on_change_with_course_completed(self):
        return not (self.is_active or self.discontinued)


class InpatientMedicationAdminTimes(models.Model):
    _description = 'Inpatient Medication Admin Times'
    _name = "medical.inpatient.medication.admin_time"

    name = fields.Many2one(
        'medical.inpatient.medication',
        'Medication'
    )
    admin_time = fields.Datetime(
        "Time"
    )
    dose = fields.Float(
        'Dose',
        help='Amount of medication (eg, 250 mg) per dose'
    )
    dose_unit = fields.Many2one(
        'medical.dose.unit',
        'dose unit',
        help='Unit of measure for the medication to be taken'
    )
    remarks = fields.Text(
        'Remarks',
        help='specific remarks for this dose'
    )


class InpatientMedicationLog(models.Model):
    _description = 'Inpatient Medication Log History'
    _name = "medical.inpatient.medication.log"

    @api.model
    def _default_health_professional(self):
        # pool = Pool()
        return self.env['res.partner'].get_health_professional()

    @api.model
    def _default_admin_time(self):
        return datetime.now()

    name = fields.Many2one(
        'medical.inpatient.medication',
        'Medication'
    )
    admin_time = fields.Datetime(
        "Date",
        readonly=True,
        default=_default_admin_time
    )
    health_professional = fields.Many2one(
        'res.partner',
        'Health Professional',
        domain=[('is_healthprof', '=', True)],
        readonly=True,
        default=_default_health_professional
    )
    dose = fields.Float(
        'Dose',
        help='Amount of medication (eg, 250 mg) per dose'
    )
    dose_unit = fields.Many2one(
        'medical.dose.unit',
        'dose unit',
        help='Unit of measure for the medication to be taken'
    )
    remarks = fields.Text(
        'Remarks',
        help='specific remarks for this dose'
    )

    @api.constrains('health_professional')
    def validate(self):
        super(InpatientMedicationLog, self).validate()
        for record in self:
            record.check_health_professional()

    def check_health_professional(self):
        if not self.health_professional:
            raise UserError(
                _(
                    'No health professional associated to this user!'
                ))


class InpatientDiet(models.Model):
    _description = 'Inpatient Diet'
    _name = "medical.inpatient.diet"

    name = fields.Many2one(
        'medical.inpatient.registration',
        'Registration Code'
    )
    diet = fields.Many2one(
        'medical.diet.therapeutic',
        'Diet',
        required=True
    )
    remarks = fields.Text(
        'Remarks / Directions',
        help='specific remarks for this diet / patient'
    )


class InpatientMeal(models.Model):
    _description = 'Inpatient Meal'
    _name = "medical.inpatient.meal"

    @api.model
    def _default_institution(self):
        # res.partner
        HealthInst = self.env['res.partner']
        institution = HealthInst.get_institution()
        return institution

    name = fields.Many2one(
        'product.product',
        'Food',
        required=True,
        help='Food'
    )

    diet_therapeutic = fields.Many2one(
        'medical.diet.therapeutic',
        'Diet'
    )

    diet_belief = fields.Many2one(
        'medical.diet.belief',
        'Belief'
    )

    diet_vegetarian = fields.Many2one(
        'medical.vegetarian_types',
        'Vegetarian'
    )

    institution = fields.Many2one(
        'res.partner',
        'Institution',
        domain=[('is_institution', '=', True)],
        default=_default_institution
    )

    def _get_name(self):
        if self.name:
            return self.name.name


class InpatientMealOrderItem(models.Model):
    _description = 'Inpatient Meal Item'
    _name = "medical.inpatient.meal.order.item"

    name = fields.Many2one(
        'medical.inpatient.meal.order',
        'Meal Order'
    )

    meal = fields.Many2one(
        'medical.inpatient.meal',
        'Meal'
    )

    remarks = fields.Char(
        'Remarks'
    )


class InpatientMealOrder(models.Model):
    _description = 'Inpatient Meal Order'
    _name = "medical.inpatient.meal.order"

    @api.model
    def _default_order_date(self):
        return datetime.now()

    @api.model
    def _default_health_professional(self):
        # pool = Pool()
        return self.env['res.partner'].get_health_professional()

    name = fields.Many2one(
        'medical.inpatient.registration',
        'Registration Code',
        domain=[('state', '=', 'hospitalized')],
        required=True
    )

    mealtime = fields.Selection(
        [
            ('none', ''),
            ('breakfast', 'Breakfast'),
            ('lunch', 'Lunch'),
            ('dinner', 'Dinner'),
            ('snack', 'Snack'),
            ('special', 'Special order'),
        ],
        'Meal time',
        required=True,
        sort=False
    )

    meal_item = fields.One2many(
        'medical.inpatient.meal.order.item',
        'name',
        'Items'
    )

    meal_order = fields.Char(
        'Order',
        readonly=True
    )

    health_professional = fields.Many2one(
        'res.partner',
        'Health Professional',
        domain=[('is_healthprof', '=', True)],
        default=_default_health_professional
    )

    remarks = fields.Text(
        'Remarks'
    )

    meal_warning = fields.Boolean(
        'Warning',
        help="The patient has special needs on meals"
    )

    meal_warning_ack = fields.Boolean(
        'Ack',
        help="Check if you have verified the warnings on the"
             " patient meal items"
    )

    order_date = fields.Datetime(
        'Date',
        help='Order date',
        required=True,
        default=_default_order_date
    )

    state = fields.Selection(
        [
            ('none', ''),
            ('draft', 'Draft'),
            ('cancelled', 'Cancelled'),
            ('ordered', 'Ordered'),
            ('processing', 'Processing'),
            ('done', 'Done'),
        ],
        'Status',
        readonly=True,
        default='draft'
    )

    @api.model_create_multi
    def create(self, vals_list):
        vals_list = [x.copy() for x in vals_list]
        for values in vals_list:
            if not values.get('meal_order'):
                values['meal_order'] = self.env['ir.sequence'].next_by_code('medical.inpatient.meal.order')
        return super(InpatientMealOrder, self).create(vals_list)

    @api.constrains('health_professional', 'meal_warning', 'meal_warning_ack')
    def validate(self):
        super(InpatientMealOrder, self).validate()
        for meal_order in self:
            meal_order.check_meal_order_warning()
            meal_order.check_health_professional()

    def check_meal_order_warning(self):
        if not self.meal_warning_ack and self.meal_warning:
            raise UserError(
                _(
                    '===== MEAL WARNING ! =====\n\n\n'
                    'This patient has special meal needs \n\n'
                    'Check and acknowledge that\n'
                    'the meal items in this order are correct \n\n'
                ))

    def check_health_professional(self):
        if not self.health_professional:
            raise UserError(
                _(
                    'No health professional associated to this user!'
                ))

    @api.depends('name')
    def on_change_name(self):
        if self.name:
            # Trigger the warning if the patient 
            # has special needs on meals (religion / philosophy )
            if (self.name.patient.vegetarian_type or
                    self.name.patient.diet_belief):
                self.meal_warning = True
                self.meal_warning_ack = False

    _sql_constraints = [
        ('meal_order_uniq', 'unique (meal_order)', 'The Meal Order code already exists!'),
    ]

    def button_generate(self):
        self.ensure_one()
        self.write({'state': 'ordered'})

    def button_cancel(self):
        self.ensure_one()
        self.write({'state': 'cancelled'})

    def button_done(self):
        self.ensure_one()
        self.write({'state': 'done'})

#Evaluation
class PatientEvaluation(models.Model):
    _name = 'medical.patient.evaluation'
    _description = 'Patient Evaluation'
    #_inherit = 'medical.patient.evaluation'
    inpatient_registration_code = fields.Many2one('medical.inpatient.registration',
                                                  'IPC',
                                                  help="Enter the patient hospitalization code")
    description = fields.Text('Remark')

# ECG
class PatientECG(models.Model):
    _name = 'medical.patient.ecg'
    _description = 'Patient ECG'
    #_inherit = 'medical.patient.ecg'
    inpatient_registration_code = fields.Many2one('medical.inpatient.registration',
                                                  'Inpatient Registration',
                                                  help="Enter the patient hospitalization code")
    description = fields.Text('Remark')