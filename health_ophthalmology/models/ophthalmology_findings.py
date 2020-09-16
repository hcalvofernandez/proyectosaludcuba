# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta, date


class OphthalmologyFindings(models.Model):
    _name = 'gnuhealth.ophthalmology.findings'
    _description = 'OphthalmologyFindings'

    # Findings associated to a particular evaluation
    name = fields.Many2one('gnuhealth.ophthalmology.evaluation',
        'Evaluation', readonly=True)

    # Structure
    structure = [
        ('lid', 'Lid'),
        ('ncs', 'Naso-lacrimal system'),
        ('conjuctiva', 'Conjunctiva'),
        ('cornea', 'Cornea'),
        ('anterior_chamber', 'Anterior Chamber'),
        ('iris', 'Iris'),
        ('pupil', 'Pupil'),
        ('lens', 'Lens'),
        ('vitreous', 'Vitreous'),
        ('fundus_disc', 'Fundus Disc'),
        ('macula', 'Macula'),
        ('fundus_background', 'Fundus background'),
        ('fundus_vessels', 'Fundus vessels'),
        ('other', 'Other'),
        ]

    eye_structure = fields.Selection(structure,
        'Structure',help="Affected eye structure",sort=False)

    affected_eye = fields.Selection([
            ("right","right"),
            ("left","left"),
            ("both","both"),
        ],'Eye',help="Affected eye",sort=False)

    finding = fields.Char('Finding')