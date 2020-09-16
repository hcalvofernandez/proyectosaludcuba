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

# -*- coding: utf-8 -*-


from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date
import logging
from psycopg2 import sql, extras
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.tools.translate import _
from odoo.tools import email_re, email_split
from odoo.exceptions import UserError, AccessError
from odoo.addons.phone_validation.tools import phone_validation
from collections import OrderedDict
STATES = {'done': [('readonly', True)]}


class OphthalmologyEvaluation(models.Model):
    _name = 'gnuhealth.ophthalmology.evaluation'
    _description = 'Ophthalmology Evaluation'

    @api.model
    def default_health_professional(self):
        loging_user = self.env.user
        health_professional = loging_user.partner_id
        return health_professional

    @api.model
    def default_visit_date(self):
        return fields.Datetime.now

    @api.model
    def default_state(self):
        return 'in_progress'

    name = fields.Char(string="Name")

    patient = fields.Many2one(
        comodel_name='medical.patient', string='Patient', required=True)

    visit_date = fields.Datetime(
        string='Date', help="Date of Consultation",
        required=False, default=fields.Datetime.now)

    computed_age = fields.Char(
        string='Age', help="Computed patient age at the moment of the evaluation",
        computed='patient_age_at_evaluation', store=True)

    gender = fields.Selection(
        string='Gender',
        selection=[('male', 'Male'),
                   ('female', 'Female'), ],
        required=False, computed='get_patient_gender',)

    health_professional = fields.Many2one(comodel_name='res.partner', string='Health Professional', readonly=True,
                                          help="Health professional / Ophthalmologist / OptoMetrist",  default=default_health_professional)

    # there are two types of charts, a meter chart.. 6/.. val
    # and ft chart.. 200/...
    snellen_chart = [
        ('6_6', '6/6'),
        ('6_9', '6/9'),
        ('6_12', '6/12'),
        ('6_18', '6/18'),
        ('6_24', '6/24'),
        ('6_36', '6/36'),
        ('6_60', '6/60'),
        ('5_60', '5/60'),
        ('4_60', '4/60'),
        ('3_60', '3/60'),
        ('2_60', '2/60'),
        ('1_60', '1/60'),
        ('1_meter_fc', '1 Meter FC'),
        ('1_2_meter_fc', '1/2 Meter FC'),
        ('hmfc', 'HMCF'),
        ('p_l', 'P/L'),
    ]

    # Near vision chart
    near_vision_chart = [
        ('N6', 'N6'),
        ('N8', 'N8'),
        ('N12', 'N12'),
        ('N18', 'N18'),
        ('N24', 'N24'),
        ('N36', 'N36'),
        ('N60', 'N60'),
    ]
    # vision test using snellen chart
    rdva = fields.Selection(snellen_chart, 'RDVA',
                            help="Right Eye Vision of Patient without aid",
                            sort=False, states=STATES)
    ldva = fields.Selection(snellen_chart, 'LDVA',
                            help="Left Eye Vision of Patient without aid",
                            sort=False, states=STATES)
    # vision test using pinhole accurate manual testing
    rdva_pinhole = fields.Selection(snellen_chart, 'RDVA',
                                    help="Right Eye Vision Using Pin Hole",
                                    sort=False, states=STATES)
    ldva_pinhole = fields.Selection(snellen_chart, 'LDVA',
                                    help="Left Eye Vision Using Pin Hole",
                                    sort=False, states=STATES)
    # vison testing with glasses just to assess what the patient sees with
    # his existing aid # useful esp with vision syndromes that are not
    # happening because of the lens
    rdva_aid = fields.Selection(snellen_chart, 'RDVA AID',
                                help="Vision with glasses or contact lens",
                                sort=False, states=STATES)
    ldva_aid = fields.Selection(snellen_chart, 'LDVA AID',
                                help="Vision with glasses or contact lens",
                                sort=False, states=STATES)

    # spherical
    rspherical = fields.Float('SPH', help='Right Eye Spherical', states=STATES)
    lspherical = fields.Float('SPH', help='Left Eye Spherical', states=STATES)

    # cylinder
    rcylinder = fields.Float('CYL', help='Right Eye Cylinder', states=STATES)
    lcylinder = fields.Float('CYL', help='Left Eye Cylinder', states=STATES)

    # axis
    raxis = fields.Float('Axis', help='Right Eye Axis', states=STATES)
    laxis = fields.Float('Axis', help='Left Eye Axis', states=STATES)

    # near vision testing .... you will get it when u cross 40 :)
    # its also thinning of the lens.. the focus falls behind the retina
    # in case of distant vision the focus does not reach retina

    rnv_add = fields.Float('NV Add', help='Right Eye Best Corrected NV Add',
                           states=STATES)
    lnv_add = fields.Float(
        'NV Add', help='Left Eye Best Corrected NV Add', states=STATES)

    rnv = fields.Selection(near_vision_chart, 'RNV',
                           help="Right Eye Near Vision", sort=False,
                           states=STATES)
    lnv = fields.Selection(near_vision_chart, 'LNV',
                           help="Left Eye Near Vision", sort=False,
                           states=STATES)

    # after the above tests the optometrist or doctor comes to a best conclusion
    # best corrected visual acuity
    # the above values are from autorefraction
    # the doctors decision is final
    # and there could be changes in values of cylinder, spherical and axis
    # these values will go into final prescription of glasses or contact lens
    # by default these values should be auto populated
    # and should be modifiable by an ophthalmologist
    rbcva_spherical = fields.Float('SPH',
                                   help='Right Eye Best Corrected Spherical', states=STATES)
    lbcva_spherical = fields.Float('SPH',
                                   help='Left Eye Best Corrected Spherical', states=STATES)

    rbcva_cylinder = fields.Float('CYL',
                                  help='Right Eye Best Corrected Cylinder', states=STATES)
    lbcva_cylinder = fields.Float('CYL',
                                  help='Left Eye Best Corrected Cylinder', states=STATES)

    rbcva_axis = fields.Float('Axis',
                              help='Right Eye Best Corrected Axis', states=STATES)
    lbcva_axis = fields.Float('Axis',
                              help='Left Eye Best Corrected Axis', states=STATES)

    rbcva = fields.Selection(snellen_chart, 'RBCVA',
                             help="Right Eye Best Corrected VA", sort=False, states=STATES)
    lbcva = fields.Selection(snellen_chart, 'LBCVA',
                             help="Left Eye Best Corrected VA", sort=False, states=STATES)

    rbcva_nv_add = fields.Float('BCVA - Add',
                                help='Right Eye Best Corrected NV Add', states=STATES)
    lbcva_nv_add = fields.Float('BCVA - Add',
                                help='Left Eye Best Corrected NV Add', states=STATES)

    rbcva_nv = fields.Selection(near_vision_chart, 'RBCVANV',
                                help="Right Eye Best Corrected Near Vision",
                                sort=False, states=STATES)
    lbcva_nv = fields.Selection(near_vision_chart, 'LBCVANV',
                                help="Left Eye Best Corrected Near Vision",
                                sort=False, states=STATES)

    # some other tests of the eyes
    # useful for diagnosis of glaucoma a disease that builds up
    # pressure inside the eye and destroy the retina
    # its also called the silent vision stealer
    # intra ocular pressure
    # there are three ways to test iop
    #   SCHIOTZ
    #   NONCONTACT TONOMETRY
    #   GOLDMANN APPLANATION TONOMETRY

    # notes by the ophthalmologist or optometrist
    notes = fields.Text('Notes', states=STATES)

    # Intraocular Pressure
    iop_method = fields.Selection([
        ('nct', 'Non-contact tonometry'),
        ('schiotz', 'Schiotz tonometry'),
        ('goldmann', 'Goldman tonometry'),
    ], 'Method', help='Tonometry / Intraocular pressure reading method',
        states=STATES)

    riop = fields.Float('RIOP', digits=(2, 1),
                        help="Right Intraocular Pressure in mmHg", states=STATES)

    liop = fields.Float('LIOP', digits=(2, 1),
                        help="Left Intraocular Pressure in mmHg", states=STATES)

    findings = fields.One2many(
        'gnuhealth.ophthalmology.findings', 'name',
        'Findings', states=STATES)

    state = fields.Selection([
        ('in_progress', 'In progress'),
        ('done', 'Done'),
    ], 'State', readonly=True, sort=False, default=default_state)

    signed_by = fields.Many2one(
        'res.partner', 'Signed by', readonly=True,
        #     states={'invisible': [('state','==', 'in_progress')]},
        help="Health Professional that finished the patient evaluation")

    @api.onchange('patient')
    def patient_age_at_evaluation(self):
        if (self.patient.birthdate_date and self.visit_date):
            rdelta = relativedelta(self.visit_date.date(),
                                   self.patient.birthdate_date)
            years_months_days = str(rdelta.years) + 'y ' \
                + str(rdelta.months) + 'm ' \
                + str(rdelta.days) + 'd'
            self.computed_age = years_months_days

    @api.onchange('patient')
    def get_patient_gender(self):
        self.gender = self.patient.gender

    # @classmethod
    # def search_patient_gender(self, name, clause):
    #     res = []
    #     value = clause[2]
    #     res.append(('patient.name.gender', clause[1], value))
    #     return res

    @api.depends('rdva')
    def on_change_with_rbcva(self):
        return self.rdva

    @api.depends('ldva')
    def on_change_with_lbcva(self):
        return self.ldva

    @api.depends('rcylinder')
    def on_change_with_rbcva_cylinder(self):
        return self.rcylinder

    @api.depends('lcylinder')
    def on_change_with_lbcva_cylinder(self):
        return self.lcylinder

    @api.depends('raxis')
    def on_change_with_rbcva_axis(self):
        return self.raxis

    @api.depends('laxis')
    def on_change_with_lbcva_axis(self):
        return self.laxis

    @api.depends('rspherical')
    def on_change_with_rbcva_spherical(self):
        return self.rspherical

    @api.depends('lspherical')
    def on_change_with_lbcva_spherical(self):
        return self.lspherical

    @api.depends('rnv_add')
    def on_change_with_rbcva_nv_add(self):
        return self.rnv_add

    @api.depends('lnv_add')
    def on_change_with_lbcva_nv_add(self):
        return self.lnv_add

    @api.depends('rnv')
    def on_change_with_rbcva_nv(self):
        return self.rnv

    @api.depends('lnv')
    def on_change_with_lbcva_nv(self):
        return self.lnv

    # Show the gender and age upon entering the patient
    # These two are function fields (don't exist at DB level)

    @api.depends('patient')
    def on_change_patient(self):
        gender = None
        age = ''
        self.gender = self.patient.gender
        self.computed_age = self.patient.age

    def end_evaluation(self):
        # Change the state of the evaluation to "Done"
        loging_user = self.env.user
        signing_hp = loging_user.partner_id
        self.state = 'done'
        self.signed_by = signing_hp
