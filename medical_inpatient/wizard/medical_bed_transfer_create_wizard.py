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

__all__ = ['CreateBedTransfer']


class CreateBedTransfer(models.TransientModel):
    """
    Create Bed Transfer.
    """
    _name = 'medical.bed.transfer.create'
    _description = 'Create Bed Transfer'
    newbed = fields.Many2one(
        'medical.hospital.bed',
        'New Bed',
        required=True,
        index=True
    )
    reason = fields.Char(
        'Reason',
        required=True
    )
    orig_bed_state = fields.Selection(
        [
            ('none', ''),
            ('free', 'Free'),
            ('reserved', 'Reserved'),
            ('occupied', 'Occupied'),
            ('to_clean', 'Needs cleaning'),
            ('na', 'Not available'),
        ], 'Bed of origin Status',
        sort=False,
        default='to_clean',
        required=True
    )
    def button_create_bed_transfer(self):
        inpatient_registrations = self.env['medical.inpatient.registration']
        bed = self.env['medical.hospital.bed']
        registrations = inpatient_registrations.browse(self.env.context['active_ids'])
        # Don't allow mass changes. Work on a single record
        if len(registrations) > 1:
            raise UserError(
                _(
                    'You have chosen more than 1 records. Please choose only one!'
                ))
        registration = registrations[0]
        current_bed = registration.bed
        destination_bed = self.newbed
        reason = self.reason
        orig_bed_state = self.orig_bed_state
        # Check that the new bed is free
        if destination_bed.state == 'free':
            # Update bed status with the one given in the transfer
            current_bed.write({'state': orig_bed_state})
            # Set as occupied the new bed
            destination_bed.write({'state': 'occupied'})
            # Update the hospitalization record
            hospitalization_info = {}
            hospitalization_info['bed'] = destination_bed
            # Update the hospitalization data
            transfers = []
            transfers.append(('create', [{
                'transfer_date': datetime.now(),
                'bed_from': current_bed.id,
                'bed_to': destination_bed.id,
                'reason': reason,
            }]))
            hospitalization_info['bed_transfers'] = transfers
            registration.write(hospitalization_info)
        else:
            raise UserError(
                _(
                    'Destination bed is unavailable!'
                ))
        return {'type': 'ir.actions.act_window_close'}
