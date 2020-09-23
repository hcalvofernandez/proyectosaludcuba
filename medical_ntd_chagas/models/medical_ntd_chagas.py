# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ChagasDUSurvey(models.Model):
    _name = 'medical.chagas_du_survey'
    _description = 'Chagas DU Entomological Survey'

    name = fields.Char('Survey Code',
                       readonly=True,
                       help="Survey Code")

    survey_date = fields.Date('Date',
                              default=fields.Date.today(),
                              required=True)
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

    du = fields.Many2one('medical.du',
                         'DU',
                         required=True,
                         index=True,
                         copy=False,
                         help="Domiciliary Unit")

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

    triatomines = fields.Boolean('Triatomines',
                                 default=False,
                                 help="Check this box if triatomines were found")

    vector = fields.Selection([
        ('None', ''),
        ('t_infestans', 'T. infestans'),
        ('t_brasilensis', 'T. brasilensis'),
        ('r_prolixus', 'R. prolixus'),
        ('t_dimidiata', 'T. dimidiata'),
        ('p_megistus', 'P. megistus'),
        ], 'Vector',
        help="Vector",
        sort=False,
        default='t_infestans')

    nymphs = fields.Boolean('Nymphs',
                            default=False,
                            help="Check this box if triatomine nymphs were found")

    t_in_house = fields.Boolean('Domiciliary',
                                default=False,
                                help="Check this box if triatomines were found inside the house")

    t_peri = fields.Boolean('Peri-Domiciliary',
                            default=False,
                            help="Check this box if triatomines were found in the peridomiciliary area")

    dfloor = fields.Boolean('Floor',
                            default=False,
                             help="Current floor can host triatomines")
    dwall = fields.Boolean('Walls',
                           default=False,
                           help="Wall materials or state can host triatomines")
    droof = fields.Boolean('Roof',
                           default=False,
                           help="Roof materials or state can host triatomines")
    dperi = fields.Boolean('Peri-domicilary',
                           help="Peri domiciliary area can host triatomines")

    bugtraps = fields.Boolean('Bug traps',
                              default=False,
                              help="The DU has traps to detect triatomines")

    du_fumigation = fields.Boolean('Fumigation',
                                   default=False,
                                   help="The DU has been fumigated")

    fumigation_date = fields.Date('Fumigation Date',
                                  help="Last Fumigation Date",
                                  invisible=True,
                                  states={'du_fumigation': [('invisible', False)]})

    du_paint = fields.Boolean('Insecticide Paint',
                              default=False,
                              help="The DU has been treated with insecticide-containing paint")

    paint_date = fields.Date('Paint Date',
                             help="Last Paint Date",
                             invisible=True,
                             states={'du_paint': [('invisible', False)]})

    observations = fields.Text('Observations',
                               help="Observations")

    next_survey_date = fields.Date('Next survey',
                                   default=fields.Date.today())

    company_id = fields.Many2one('res.company',
                                 string='Company',
                                 index=True,
                                 required=True,
                                 default=lambda self: self.env.company.id)

    user_id = fields.Many2one(
                             'res.users',
                             "Approved by",
                             default=lambda self: self.env.uid,
                             readonly=True,
                             copy=False)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('medical.chagas_du_survey')
        return super(ChagasDUSurvey, self).create(vals)

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


