# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class DengueDUSurvey(models.Model):
    _name = 'medical.dengue_du_survey'
    _description = 'Dengue DU Survey'

    name = fields.Char('Code',
                       readonly=True,
                       help="Survey Code")

    du = fields.Many2one('medical.du',
                         'DU',
                         required=True,
                         index=True,
                         copy=False,
                         help="Domiciliary Unit")

    survey_date = fields.Date('Date',
                              default=fields.Date.today(),
                              required=True)

    du_status = fields.Selection([
        ('None', ''),
        ('initial', 'Initial'),
        ('unchanged', 'Unchanged'),
        ('better', 'Improved'),
        ('worse', 'Worsen'),
        ],
        'Status',
        help="DU status compared to last visit",
        required=True,
        sort=False,
        default='initial')

    ovitraps = fields.Boolean(
        'Ovitraps',
        default=False,
        help="Check if ovitraps are in place")

    aedes_larva = fields.Boolean(
        'Larvae',
        default=False,
        help="Check this box if larvae were found inside the house")

    larva_in_house = fields.Boolean(
        'Domiciliary',
        default=False,
        help="Check this box if larvae were found inside the house")

    larva_peri = fields.Boolean(
        'Peri-Domiciliary',
        default=False,
        help="Check this box if larva were found in the peridomiciliary area")

    old_tyres = fields.Boolean(
        'Tyres',
        default=False,
        help="Old vehicle tyres found")

    animal_water_container = fields.Boolean(
        'Animal Water containers',
        default=False,
        help="Animal water containers not scrubbed or clean")

    flower_vase = fields.Boolean(
        'Flower vase',
        default=False,
        help="Flower vases without scrubbing or cleaning")

    potted_plant = fields.Boolean(
        'Potted Plants',
        default=False,
        help="Potted Plants with saucers")

    tree_holes = fields.Boolean(
        'Tree holes',
        default=False,
        help="unfilled tree holes")

    rock_holes = fields.Boolean(
        'Rock holes',
        default=False,
        help="unfilled rock holes")

    du_fumigation = fields.Boolean(
        'Fumigation',
        default=False,
        help="The DU has been fumigated")

    fumigation_date = fields.Date(
        'Fumigation Date',
        help="Last Fumigation Date",
        invisible=True,
        states={'du_fumigation': [('invisible', False)]})

    observations = fields.Text('Observations')

    next_survey_date = fields.Date('Next survey')

    user_id = fields.Many2one(
                             'res.users',
                             "Approved by",
                             default=lambda self: self.env.uid,
                             readonly=True,
                             copy=False)

    company_id = fields.Many2one('res.company',
                                 string='Company',
                                 index=True,
                                 required=True,
                                 default=lambda self: self.env.company.id)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In progress'),
        ('close', 'Closed'),
        ('cancel', 'Cancelled')],
        default='draft',
        string='State',
        copy=False,
        tracking=True,
        required=True,
        readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('medical.dengue_du_survey')
        return super(DengueDUSurvey, self).create(vals)

    def button_progress(self):
        for record in self:
            record.write({
                        'state': 'in_progress'
                        })

    def button_close(self):
        for record in self:
            record.write({
                        'state': 'close'
                        })

    def button_cancelled(self):
        for record in self:
            record.write({
                        'state': 'cancel'
                        })

    def button_draft(self):
        for record in self:
            record.write({
                        'state': 'draft'
                        })





