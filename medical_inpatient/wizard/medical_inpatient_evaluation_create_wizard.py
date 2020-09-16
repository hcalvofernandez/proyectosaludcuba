# -*- coding: utf-8 -*-
##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2020 Luis Falcon <lfalcon@gnusolidario.org>
#    Copyright (C) 2011-2020 GNU Solidario <health@gnusolidario.org>
#
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
from odoo import models, fields, api
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.tools.translate import _

__all__ = ['CreateInpatientEvaluation']


class CreateInpatientEvaluation(models.TransientModel):
    """
    Create Inpatient Evaluation.
    """
    _name = 'medical.inpatient.evaluation.create'
    _description = 'Create Inpatient Evaluation'
    def do_inpatient_evaluation(self):
        self.ensure_one()
        inpatient_registrations = self.env['medical.inpatient.registration']
        registrations = inpatient_registrations.browse(self.env.context['active_id'])
        if not registrations:
            raise UserError(
                _(
                    'You need to select an inpatient registration record!'
                ))
        patient = registrations[0].patient.id
        inpatient_registration_code = registrations[0].id
        evaluation_type = 'inpatient'
        view_id = self.env.ref('medical.medical_patient_evaluation_view').id
        return {
            'name': _('Patient Evaluation'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'medical.patient.evaluation',
            'view_id': view_id,
            'views': [(view_id, 'form')],
            'target': 'new',
            'context': {
                'default_patient': patient,
                'default_inpatient_registration_code': inpatient_registration_code,
                'default_evaluation_type': evaluation_type,
            }
        }
