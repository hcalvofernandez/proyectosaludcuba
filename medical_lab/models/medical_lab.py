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
from odoo import models, fields, api, _
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


class MedicalPatientDisease(models.Model):
    _inherit = 'medical.patient.disease'
    _description = 'Patient Conditions History'

    lab_confirmed = fields.Boolean(
        string='Lab Confirmed',
        help='Confirmed by laboratory test'
    )

    lab_test = fields.Many2one(
        comodel_name='medical.lab.test.result',
        string='Lab Test',
        # domain=[
        #     ('patient_id', '=', 'name')
        # ],
        depends=['name'],
        # states={'invisible': Not(Bool(Eval('lab_confirmed')))},
        help='Lab test that confirmed the condition'
    )


class MedicalPatientLabTest(models.Model):
    _name = 'medical.patient.lab.test'
    _description = 'Patient Lab Test'

    name = fields.Char(
        string='Order',
        readonly=True,
        required=True,
        copy=False,
        default='New'
    )
    test_type = fields.Many2one(
        comodel_name='medical.lab.test.type',
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
    urgent = fields.Boolean(
        string='Urgent'
    )
    category = fields.Many2one(
        comodel_name='medical.lab.categories',
        string='Category',
        help='Category of this lab test'
    )
    test_result = fields.One2many(
        comodel_name='medical.lab.test.result',
        inverse_name='test_request',
        string='Result'
    )
    result_count = fields.Char(
        string='Result'
    )

    def get_result(self):
        self.ensure_one()
        result_id = self.test_result.id
        view_id = self.env.ref('medical_lab.medical_lab_test_result_form').id
        return {
            'name': _('Lab Test Result'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'medical.lab.test.result',
            'res_id': result_id,
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'context': {
                'default_test_request': self.id,
                'default_patient': self.patient_id.id,
                'default_date_requested': self.date,
                'default_test': self.test_type.id
            }
        }


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
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                self._name
            ) or 'New'
        result = super(MedicalPatientLabTest, self).create(vals)
        return result


class MedicalLabTestResult(models.Model):
    _name = 'medical.lab.test.result'
    _description = 'Lab Test Results'

    name = fields.Char(
        string='ID',
        help="Lab result ID",
        readonly=True,
        required=True,
        copy=False,
        default='New'
    )
    test = fields.Many2one(
        comodel_name='medical.lab.test.type',
        string='Test type',
        help="Lab test type",
        readonly=True,
        required=True,
        index=True
    )
    patient = fields.Many2one(
        comodel_name='medical.patient',
        string='Patient',
        help="Patient ID",
        required=True,
        readonly=True,
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
    value = fields.One2many(
        comodel_name='medical.lab.test.value',
        inverse_name='test_result',
        string='Value Critearea'
    )
    date_requested = fields.Datetime(
        string='Date requested',
        required=True,
        readonly=True,
        index=True
    )
    date_analysis = fields.Datetime(
        string='Date of the Analysis',
        index=True
    )
    test_request = fields.Many2one(
        comodel_name='medical.patient.lab.test',
        readonly=True,
        string='Request'
    )
    pathology = fields.Many2one(
        comodel_name='medical.pathology',
        string='Pathology',
        help='Pathology confirmed / associated to this lab test.'
    )
    analytes_summary = fields.Text(
        string='Summary'
        # ,
        # compute='get_analytes_summary'
    )

    @api.model
    def default_get(self, fields):
        res = super(MedicalLabTestResult, self).default_get(fields)
        res.update(
            {
                'date_analysis': datetime.now()
            }
        )
        return res

    # def get_analytes_summary(self):
    #     summ = ""
    #     for analyte in self.critearea:
    #         if analyte.result or analyte.result_text:
    #             res = ""
    #             res_text = ""
    #             if analyte.result_text:
    #                 res_text = analyte.result_text
    #             if analyte.result:
    #                 res = str(analyte.result) + " "
    #             summ = summ + analyte.name + " " + \
    #                 res + res_text + "\n"
    #     self.analytes_summary = summ

    _sql_constraints = [
        (
            'id_uniq',
            'unique(name)',
            'The test ID code must be unique'
        )
    ]

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                self._name
            ) or 'New'
        result = super(MedicalLabTestResult, self).create(vals)
        return result

    @api.onchange('test')
    def onchange_test(self):
        if self.test and self.test.critearea:
            value_ids = self.test.critearea.filtered(
                lambda r: not r.test
            )
            value_id = value_ids[0] if value_ids else False
            self.value = [
                (0, 0, {
                    'name': line.name,
                    'lower_limit': line.lower_limit,
                    'upper_limit': line.upper_limit,
                    'units': line.units
                }) for line in value_ids
            ]


class MedicalLabTestValue(models.Model):
    _name = 'medical.lab.test.value'
    _description = 'Lab Test Result Value'

    result = fields.Float(
        string='Value'
    )
    result_text = fields.Char(
        string='Result - Text',
        help='Non-numeric results. For'
        'example qualitative values, morphological, colors ...'
    )
    warning = fields.Boolean(
        string='Warn',
        help='Warns the patient about this'
        ' analyte result'
        ' It is useful to contextualize the result to each patient status'
        ' like age, sex, comorbidities, ...'
    )
    test_result = fields.Many2one(
        comodel_name='medical.lab.test.result',
        string='Test Result'
    )
    name = fields.Char(
        string='Analyte',
        required=True,
        index=True,
        translate=True
    )
    lower_limit = fields.Float(
        string='Lower Limit'
    )
    upper_limit = fields.Float(
        string='Upper Limit'
    )
    units = fields.Many2one(
        comodel_name='medical.lab.test.units',
        readonly=True,
        string='Units'
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

    @api.depends('result')
    def on_change_with_warning(self):
        if (self.result and self.lower_limit):
            if (self.result < self.lower_limit):
                self.warning = True

        if (self.result and self.upper_limit):
            if (self.result > self.upper_limit):
                self.warning = True


class MedicalLabCategories(models.Model):
    _name = 'medical.lab.categories'
    _description = 'Lab Test Categories'

    name = fields.Char(
        string='Category',
        index=True
    )
    detail = fields.Char(
        string='Detail',
        index=True
    )
    conditions = fields.Char(
        string='Conditions',
        index=True
    )

    sql_constraints = [
        (
            'name_uniq',
            'unique(name)',
            'The Category name must be unique'
        )
    ]


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


class MedicalLabTestType(models.Model):
    _name = 'medical.lab.test.type'
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
        res = super(MedicalLabTestType, self).default_get(fields)
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


class MedicalLabTestCritearea(models.Model):
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
    units = fields.Many2one(
        comodel_name='medical.lab.test.units',
        string='Units'
    )
    test_type_id = fields.Many2one(
        comodel_name='medical.lab.test.type',
        string='Test type',
        index=True
    )
    medical_lab_id = fields.Many2one(
        comodel_name='medical.lab.test.result',
        string='Test Cases',
        index=True
    )
    sequence = fields.Integer(
        string='Sequence'
    )

    @api.model
    def default_get(self, fields):
        res = super(MedicalLabTestCritearea, self).default_get(fields)
        res.update(
            {
                'excluded': False,
                'sequence': 1
            }
        )
        return res
