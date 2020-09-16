# -*- coding: utf-8 -*-
##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2020 Luis Falcon <falcon@medical.org>
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


class MedicalPatient(models.Model):
    _inherit = 'medical.patient'
    _description = 'Patient lab tests'

    lab_test_ids = fields.One2many(
        comodel_name='medical.patient.lab.test',
        inverse_name='patient_id',
        string='Lab Tests Required'
    )


class TestType(models.Model):
    _name = 'medical.lab.test_type'
    _description = 'Type of Lab test'

    name = fields.Char(
        string='Test',
        help="Test type, eg X-Ray, hemogram,biopsy...",
        required=True,
        index=True,
        translate=True
    )
    code = fields.Char(
        string='Code',
        help="Short name - code for the test",
        required=True,
        index=True
    )
    info = fields.Text(
        string='Description'
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Service',
        required=True
    )
    critearea = fields.One2many(
        comodel_name='medical.lab.test.critearea',
        inverse_name='test_type_id',
        string='Test Cases'
    )
    active = fields.Boolean(
        string='Active',
        index=True
    )

    @api.model
    def default_get(self, fields):
        res = super(TestType, self).default_get(fields)
        res.update(
            {
                'active': True
            }
        )
        return res

    _sql_constraints = [
        (
            'code_uniq',
            'unique(name)',
            'The Lab Test code must be unique'
        )
    ]


class Lab(models.Model):
    _name = 'medical.lab'
    _description = 'Patient Lab Test Results'

    name = fields.Char(
        string='ID',
        help="Lab result ID",
        readonly=True
    )
    test = fields.Many2one(
        comodel_name='medical.lab.test_type',
        string='Test type',
        help="Lab test type",
        required=True,
        index=True
    )
    patient = fields.Many2one(
        comodel_name='medical.patient',
        string='Patient',
        help="Patient ID",
        required=True,
        index=True
    )
    pathologist = fields.Many2one(
        comodel_name='medical.healthprofessional',
        string='Pathologist',
        help="Pathologist",
        index=True
    )
    requestor = fields.Many2one(
        comodel_name='medical.healthprofessional',
        string='Physician',
        help="Doctor who requested the test",
        index=True
    )
    results = fields.Text(
        string='Results'
    )
    diagnosis = fields.Text(
        string='Diagnosis'
    )
    critearea = fields.One2many(
        comodel_name='medical.lab.test.critearea',
        inverse_name='medical_lab_id',
        string='Lab Test Critearea'
    )
    date_requested = fields.Datetime(
        string='Date requested',
        required=True,
        index=True
    )
    date_analysis = fields.Datetime(
        string='Date of the Analysis',
        index=True
    )
    request_order = fields.Integer(
        string='Request',
        readonly=True
    )
    pathology = fields.Many2one(
        comodel_name='medical.pathology',
        string='Pathology',
        help='Pathology confirmed / associated to this lab test.'
    )
    analytes_summary = fields.Text(
        string='Summary',
        compute='get_analytes_summary'
    )

    @api.model
    def default_get(self, fields):
        res = super(Lab, self).default_get(fields)
        res.update(
            {
                'date_requested': datetime.now(),
                'date_analysis': datetime.now()
            }
        )
        return res

    def get_analytes_summary(self):
        summ = ""
        for analyte in self.critearea:
            if analyte.result or analyte.result_text:
                res = ""
                res_text = ""
                if analyte.result_text:
                    res_text = analyte.result_text
                if analyte.result:
                    res = str(analyte.result) + " "
                summ = summ + analyte.name + " " + \
                    res + res_text + "\n"
        self.analytes_summary = summ

    _sql_constraints = [
        (
            'id_uniq',
            'unique(name)',
            'The test ID code must be unique'
        )
    ]

    @api.model
    def _create_vals(self, vals):
        vals = super(Lab, self)._create_vals(vals)
        if not vals.get('name'):
            Seq = self.env['ir.sequence']
            vals['name'] = Seq.sudo().next_by_code(
                self._name,
            )
        return vals


class MedicalLabTestUnits(models.Model):
    _name = 'medical.lab.test.units'
    _description = 'Lab Test Units'

    name = fields.Char(
        string='Unit',
        index=True
    )
    code = fields.Char(
        string='Code',
        index=True
    )

    _sql_constraints = [
        (
            'name_uniq',
            'unique(name)',
            'The Unit name must be unique'
        )
    ]


class MedicalTestCritearea(models.Model):
    _name = 'medical.lab.test.critearea'
    _description = 'Lab Test Critearea'

    test = fields.Boolean(
        string='Test'
    )
    name = fields.Char(
        string='Analyte',
        required=True,
        index=True,
        translate=True
    )
    excluded = fields.Boolean(
        string='Excluded',
        help='Select this option when this analyte is excluded from the test'
    )
    result = fields.Float(
        string='Value'
    )
    result_text = fields.Char(
        string='Result - Text',
        help='Non-numeric results. For'
        'example qualitative values, morphological, colors ...'
    )
    remarks = fields.Char(
        string='Remarks'
    )
    normal_range = fields.Text(
        string='Reference'
    )
    lower_limit = fields.Float(
        string='Lower Limit'
    )
    upper_limit = fields.Float(
        string='Upper Limit'
    )
    warning = fields.Boolean(
        string='Warn',
        help='Warns the patient about this'
        ' analyte result'
        ' It is useful to contextualize the result to each patient status'
        ' like age, sex, comorbidities, ...'
    )
    units = fields.Many2one(
        comodel_name='medical.lab.test.units',
        string='Units'
    )
    test_type_id = fields.Many2one(
        comodel_name='medical.lab.test_type',
        string='Test type',
        index=True
    )
    medical_lab_id = fields.Many2one(
        comodel_name='medical.lab',
        string='Test Cases',
        index=True
    )
    sequence = fields.Integer(
        string='Sequence'
    )

    lab_warning_icon = fields.Char(
        string='Lab Warning Icon',
        compute='get_lab_warning_icon',
        default='medical-normal'
    )

    @api.model
    def get_lab_warning_icon(self):
        if (self.warning):
            self.lab_warning_icon = 'medical-warning'

    @api.model
    def default_get(self, fields):
        res = super(MedicalTestCritearea, self).default_get(fields)
        res.update(
            {
                'excluded': False,
                'sequence': 1
            }
        )
        return res

    @api.depends('result', 'lower_limit', 'upper_limit')
    def on_change_with_warning(self):
        if (self.result and self.lower_limit):
            if (self.result < self.lower_limit):
                self.warning = True

        if (self.result and self.upper_limit):
            if (self.result > self.upper_limit):
                self.warning = True


class MedicalPatientLabTest(models.Model):
    _name = 'medical.patient.lab.test'
    _description = 'Patient Lab Test'

    name = fields.Many2one(
        comodel_name='medical.lab.test_type',
        string='Test Type',
        required=True,
        index=True
    )
    date = fields.Datetime(
        string='Date',
        index=True
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('tested', 'Tested'),
            ('ordered', 'Ordered'),
            ('cancel', 'Cancel'),
        ],
        string='State',
        readonly=True,
        index=True
    )
    patient_id = fields.Many2one(
        comodel_name='medical.patient',
        string='Patient',
        required=True,
        index=True
    )
    doctor_id = fields.Many2one(
        string='Doctor',
        comodel_name='medical.healthprofessional',
        help='Doctor who Request the lab test',
        readonly=True,
    )
    request = fields.Integer(
        string='Order',
        readonly=True
    )
    urgent = fields.Boolean(
        string='Urgent'
    )

    @api.model
    def default_get(self, fields):
        res = super(MedicalPatientLabTest, self).default_get(fields)
        res.update(
            {
                'date': datetime.now(),
                'state': 'draft'
            }
        )
        return res

    @api.model
    def _create_vals(self, vals):
        vals = super(MedicalPatientLabTest, self)._create_vals(vals)
        if not vals.get('request'):
            Seq = self.env['ir.sequence']
            vals['request'] = Seq.sudo().next_by_code(
                self._name,
            )
        return vals


class PatientHealthCondition(models.Model):
    _inherit = 'medical.patient.disease'
    _description = 'Patient Conditions History'

    lab_confirmed = fields.Boolean(
        string='Lab Confirmed',
        help='Confirmed by laboratory test'
    )

    lab_test = fields.Many2one(
        comodel_name='medical.lab',
        string='Lab Test',
        # domain=[
        #     ('patient_id', '=', 'name')
        # ],
        depends=['name'],
        # states={'invisible': Not(Bool(Eval('lab_confirmed')))},
        help='Lab test that confirmed the condition'
    )
