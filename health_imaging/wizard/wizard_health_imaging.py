# -*- coding: utf-8 -*-
##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2020 Luis Falcon <lfalcon@gnuhealth.org>
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

__all__ = ['RequestImagingTest',
           'RequestPatientImagingTestStart']

class RequestImagingTest(models.TransientModel):
    'Request - Test'
    _name = 'gnuhealth.request.imaging.test'
    _table = 'gnuhealth_request_imaging_test'
    _description = "Wizard: Request - Test"
    request = fields.Many2one('gnuhealth.patient.imaging.test.request.start',
                              'Request', required=True)
    test = fields.Many2one('gnuhealth.imaging.test', 'Test', required=True)

class RequestPatientImagingTestStart(models.TransientModel):
    'Request Patient Imaging Test Start'
    _name = 'gnuhealth.patient.imaging.test.request.start'
    _description = "Wizard: Request Patient Imaging Test Start"
    date = fields.Datetime('Date',default=datetime.today())
    patient = fields.Many2one('medical.patient', 'Patient', required=True)
    doctor = fields.Many2one('res.partner', 'Doctor',
        required=True, help="Doctor who Request the lab tests.")
    tests = fields.Many2many('gnuhealth.request.imaging.test', 'request',
                           'test', 'Tests', required=True)
    urgent = fields.Boolean('Urgent')
    def default_doctor(self):
        HealthProf= self.env.get('res.partner')
        hp = HealthProf.get_health_professional()
        if not hp:
            RequestPatientImagingTestStart.raise_user_error(
                "No health professional associated to this user !")
        return hp


