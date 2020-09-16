# -*- coding: utf-8 -*-
##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    MODULE : Diagnostic Imaging
#
#    Copyright (C) 2008-2020 Luis Falcon <lfalcon@gnuhealth.org>
#    Copyright (C) 2011-2020 GNU Solidario <health@gnusolidario.org>
#    Copyright (C) 2013  Sebastián Marro <smarro@thymbra.com>
#    Copyright (C) 2020  Yadier A. De Quesada <yadierq87@gmail.com>
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

__all__ = [
    'GnuHealthSequences', 'GnuHealthSequenceSetup','ImagingTestType',
    'ImagingTest', 'ImagingTestRequest', 'ImagingTestResult']
sequences = ['imaging_request_sequence', 'imaging_sequence']

class GnuHealthSequences(models.Model ):
    "GNU Health Sequences"
    _name = "gnuhealth.sequences"
    _description = "GNU Health Sequences"
    _order = 'id,name'
    _table = 'gnuhealth_sequences'
    imaging_request_sequence =  fields.Many2one(
        'ir.sequence',
        'Imaging Request Sequence',
        domain=[('code', '=', 'gnuhealth.imaging.test.request')],
        required=True)
    imaging_sequence =   fields.Many2one(
        'ir.sequence',
        'Imaging Sequence',
        domain=[('code', '=', 'gnuhealth.imaging.test.result')],
        required=True)
    @classmethod
    def _multivalue_model(self, field):
        self.env = self.env['gnuhealth.sequence.setup']
        if field in sequences:
            return self.env.get()
        return super(GnuHealthSequences).multivalue_model(field)
    @classmethod
    def _default_imaging_request_sequence(self):
        return self.multivalue_model(
            'imaging_request_sequence').default_imaging_request_sequence()
    @classmethod
    def _default_imaging_sequence(self):
        return self.multivalue_model(
            'imaging_sequence').default_imaging_sequence()
# SEQUENCE SETUP
class GnuHealthSequenceSetup(models.Model):
    'GNU Health Sequences Setup'
    _name = 'gnuhealth.sequence.setup'
    _description = 'GNU Health Sequences Setup'
    _order = 'id,name'
    _table = 'gnuhealth_sequences_setup'
    imaging_request_sequence = fields.Many2one('ir.sequence',
                                               'Imaging Request Sequence', required=True,
                                               domain=[('code', '=', 'gnuhealth.imaging.test.request')])
    imaging_sequence = fields.Many2one('ir.sequence',
                                       'Imaging Result Sequence', required=True,
                                       domain=[('code', '=', 'gnuhealth.imaging.test.result')])
    @classmethod
    def default_imaging_request_sequence(self):
        ModelData = self.env.get('ir.model.data')
        return ModelData.get_id(
            'health_imaging', 'seq_gnuhealth_imaging_test_request')
    @classmethod
    def default_imaging_sequence(self):
        ModelData = self.env.get('ir.model.data')
        return ModelData.get_id(
            'health_imaging', 'seq_gnuhealth_imaging_test')
# END SEQUENCE SETUP , MIGRATION FROM FIELDS.PROPERTY
class ImagingTestType(models.Model):
    'Imaging Test Type'
    _name = 'gnuhealth.imaging.test.type'
    _description = 'Imaging Test Type'
    _order = 'id,name'
    _table = 'gnuhealth_imaging_test_type'
    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
class ImagingTest(models.Model, ):
    'Imaging Test'
    _name = 'gnuhealth.imaging.test'
    _description = 'Imaging Test'
    _order = 'id,name'
    _table = 'gnuhealth_imaging_test'
    code = fields.Char('Code', required=True)
    name = fields.Char('Name', required=True)
    test_type = fields.Many2one(
        'gnuhealth.imaging.test.type', 'Type',
        required=True)
    product = fields.Many2one('product.product', 'Service', required=True)
    active = fields.Boolean('Active', index=True,default=True)
class ImagingTestRequest(models.Model):
    'Imaging Test Request'
    _name = 'gnuhealth.imaging.test.request'
    _description = 'Imaging Test Request'
    _order = 'date desc,name desc'
    _table = 'gnuhealth_imaging_test_request'
    patient = fields.Many2one('medical.patient', 'Patient', required=True)
    date = fields.Datetime('Date', required=True,default=datetime.date.today())
    requested_test = fields.Many2one(
        'gnuhealth.imaging.test', 'Test',
        required=True)
    doctor = fields.Many2one('res.partner', 'Doctor', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('requested', 'Requested'),
        ('done', 'Done'),
    ], 'State', default='draft')
    comment = fields.Text('Comment')
    name = fields.Char('Request', readonly=True, required=True, copy=False, default='New')
    urgent = fields.Boolean('Urgent')
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'gnuhealth.imaging.test.request') or 'New'
        result = super(ImagingTestRequest, self).create(vals)
        return result

    def copy(self, tests, default=None):
        if default is None:
            default = {}
        default = default.copy()
        default['request'] = None
        default['date'] = datetime.date.today()
        return super(ImagingTestRequest, self).copy(tests, default=default)

    def requested(self):
        self.state = 'requested'

    #open ('health_imaging.wizard_generate_result')
    def generate_results(self):
        """ This opens the xml view specified in xml_id for the current vehicle """
        self.ensure_one()
        xml_id = self.env.context.get('xml_id')
        if xml_id:
            res = self.env['ir.actions.act_window'].for_xml_id('health_imaging', xml_id)
            res.update(
                context=dict(self.env.context,
                default_patient=self.patient.id,
                default_requested_test=self.requested_test.id,
                default_request=self.id,
                default_request_date=self.date,
                group_by=False),
                domain=[('patient', '=', self.patient.id)]
            )
            return res
        return False

    def done(self):
        self.state = 'done'

class ImagingTestResult(models.Model):
    'Imaging Test Result'
    _name = 'gnuhealth.imaging.test.result'
    _description = 'Imaging Test Result'
    _inherit = ['image.mixin']
    _order = 'date desc'
    _table = 'gnuhealth_imaging_test_result'
    name = fields.Char('Number', readonly=True, required=True, copy=False, default='New')
    patient = fields.Many2one('medical.patient', 'Patient', readonly=True)
    date = fields.Datetime('Date', required=True)
    request_date = fields.Datetime('Requested Date', readonly=True)
    requested_test = fields.Many2one(
        'gnuhealth.imaging.test', 'Test',
        required=True)
    request = fields.Many2one(
        'gnuhealth.imaging.test.request', 'Request',
        readonly=True)
    doctor = fields.Many2one('res.partner', 'Doctor',required=True)
    comment = fields.Text('Comment')
    images = fields.Many2many(comodel_name="ir.attachment", relation="m2m_ir_attachment_relation", column1="m2m_id",
                                  column2="attachment_id", string="Attachments", )
    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         'The test ID code must be unique!')]
    @api.model
    def create(self, vals):
       if vals.get('name', 'New') == 'New':
           vals['name'] = self.env['ir.sequence'].next_by_code(
               'gnuhealth.imaging.test.result') or 'New'
       result = super(ImagingTestResult, self).create(vals)
       return result
    @classmethod
    def search_rec_name(self, name, clause):
        if clause[1].startswith('!') or clause[1].startswith('not '):
            bool_op = 'AND'
        else:
            bool_op = 'OR'
        return [bool_op,
                ('patient',) + tuple(clause[1:]),
                ('name',) + tuple(clause[1:]),
                ]


