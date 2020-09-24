#!/usr/bin/env python
# -*- encoding: utf-8 -*-
###############################################################################
#
#    This software has been developed for the management of projects
#    of OBPP of Venezuela that are funded by the federal government council.
#    Copyright (C) 2013  HOATZIN
#    Aristobulo Meneses <ameneses@hoatzin.org>,
#    Ruben Bravo <rbravo@hoatzin.org>),
#    Manuel Márquez <mmarquez@hoatzin.org>,
#    Fredy Toro <ftoro@hoatzin.org>,
#    Reinaldo Carrasquero <rcarrasquero@hoatzin.org>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp.osv import orm, osv, fields
from openerp.tools.translate import _
from openerp import exceptions
import datetime
from datetime import tzinfo
from pytz import timezone

class Venezuelatz(tzinfo):

    def __unicode__(self):
        return self.tzname

    def utcoffset(self,dt):
        return datetime.timedelta(hours=-4)

    def tzname(self,dt):
        return "America/Vzla"

    def dst(self,dt):
        return datetime.timedelta(0)
Venezuelatz()
