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
from odoo import api, fields, models, _

__all__ = ['HealthInstitution', ]


class HealthInstitution(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    def get_institution(self):
        # Retrieve the institution associated to this GNU Health instance
        # That is associated to the Company.

        if self.env.company and self.env.company.partner_id.is_institution:
            return self.env.company.partner_id.id
        else:
            return False

    code = fields.Char('Code',
                       help="Institution code")

    picture = fields.Binary('Picture')

    institution_type = fields.Selection((('none', ''),
                                         ('doctor_office', 'Doctor office'),
                                         ('primary_care', 'Primary Care Center'),
                                         ('clinic', 'Clinic'),
                                         ('hospital', 'General Hospital'),
                                         ('specialized', 'Specialized Hospital'),
                                         ('nursing_home', 'Nursing Home'),
                                         ('hospice', 'Hospice'),
                                         ('rural', 'Rural facility'),
                                         ),
                                        'Type',
                                        sort=False)

    beds = fields.Integer("Beds")

    operating_room = fields.Boolean("Operating Room",
                                    help="Check this box if the institution has operating rooms",
                                    )
    or_number = fields.Integer("ORs")

    public_level = fields.Selection((('none', ''),
                                     ('private', 'Private'),
                                     ('public', 'Public'),
                                     ('mixed', 'Private - State'),
                                     ),
                                    'Public Level',
                                    sort=False)

    teaching = fields.Boolean("Teaching",
                              help="Mark if this is a teaching institution")

    heliport = fields.Boolean("Heliport")

    is_institution = fields.Boolean("Is institution")

    trauma_center = fields.Boolean("Trauma Center")

    trauma_level = fields.Selection((('none', ''),
                                     ('one', 'Level I'),
                                     ('two', 'Level II'),
                                     ('three', 'Level III'),
                                     ('four', 'Level IV'),
                                     ('five', 'Level V'),
                                     ),
                                    'Trauma Level',
                                    sort=False)

    extra_info = fields.Text("Extra Info")

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'This Institution already exists!'),
        ('code_uniq', 'unique (code)', 'This CODE already exists!'),
    ]
