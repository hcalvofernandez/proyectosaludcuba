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
from odoo.osv import expression

__all__ = ['Pathology', ]


class Pathology(models.Model):
    _description = 'Health Conditions'
    _name = 'medical.pathology'

    name = fields.Char('Name',
                       required=True,
                       translate=True,
                       help='Health condition name')

    code = fields.Char('Code',
                       required=True,
                       help='Specific Code for the Disease (eg, ICD-10)')
    # category = fields.Many2one('gnuhealth.pathology.category', 'Main Category',
    #                            help='Select the main category for this disease This is usually'
    #                                 ' associated to the standard. For instance, the chapter on the ICD-10'
    #                                 ' will be the main category for de disease')
    #
    # groups = fields.One2many('gnuhealth.disease_group.members', 'name',
    #                          'Groups', help='Specify the groups this pathology belongs. Some'
    #                                         ' automated processes act upon the code of the group')

    chromosome = fields.Char('Affected Chromosome',
                             help='chromosome number')

    protein = fields.Char('Protein involved',
                          help='Name of the protein(s) affected')

    gene = fields.Char('Gene',
                       help='Name of the gene(s) affected')

    info = fields.Text('Extra Info')

    active = fields.Boolean('Active', index=True, default=True)

    def _get_name(self):
        if self.name and self.code:
            return self.code + ' : ' + self.name

    # Search by the health condition code or the description
    @classmethod
    def search_rec_name(cls, name, clause):
        if clause[1].startswith('!') or clause[1].startswith('not '):
            bool_op = 'AND'
        else:
            bool_op = 'OR'
        return [bool_op,
                ('code',) + tuple(clause[1:]),
                ('name',) + tuple(clause[1:]),
                ]

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if operator.startswith('!') or operator.startswith('not '):
            domain = [
                ('name', operator, name),
                ('code', operator, name),
            ]
        else:
            domain = ['|',
                      ('name', operator, name),
                      ('code', operator, name),
                      ]
        rec = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(rec).with_user(name_get_uid))

    _sql_constraints = [
        ('code_uniq', 'unique (code)', 'The disease code must be unique!'),
    ]
