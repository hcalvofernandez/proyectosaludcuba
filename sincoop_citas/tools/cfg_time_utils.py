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
#    Mantenimiento y actualización por la Asociación CPUi.
#
###############################################################################

import ephem
import datetime
from pytz import timezone


class TimeUtils():
    def float2seconds(self, time=None):
        res = datetime.timedelta(
            hours=int(time), minutes=int((abs(time)-abs(int(time)))*100)
        )
        return res

    def float2time(self, time=None):
        res = {
            'hour': int(time),
            'minute': int((abs(time)-abs(int(time)))*100)
        }
        return res

    def datestr2dict(self, date=None):
        datetime_list = date.split()
        date_list = datetime_list[0].split('-')
        if len(datetime_list) > 1:
            time_list = datetime_list[1].split(':')
            datetime_dict = {
                'year': date_list[0],
                'month': date_list[1],
                'day': date_list[2],
                'hour': time_list[0],
                'minute': time_list[1],
                'seconds': time_list[2]
            }
        else:
            datetime_dict = {
                'year': date_list[0],
                'month': date_list[1],
                'day': date_list[2],
                'hour': 0,
                'minute': 0,
                'seconds': 0
            }
        return datetime_dict

    def datedict2dt(self, date=None, tzinfo=None):
        date_dt = datetime.datetime(
            int(date['year']), int(date['month']), int(date['day']),
            int(date['hour']), int(date['minute']), int(date['seconds']),
            tzinfo=tzinfo
        )
        return date_dt

    def get_season(date):
        # Convert date to month and day as integer (md), e.g. 4/21 = 421,
        # 11/17 = 1117, etc.
        m = date.month * 100
        d = date.day
        md = m + d
        if ((md > 320) and (md < 621)):
            s = 0  # spring
        elif ((md > 620) and (md < 923)):
            s = 1  # summer
        elif ((md > 922) and (md < 1223)):
            s = 2  # fall
        else:
            s = 3  # winter
        return s

    def get_dr(self, year=datetime.datetime.now().year):
        d1 = ephem.next_full_moon(
            datetime.datetime(year, 3, 21, 0, 0, 0, tzinfo=timezone('UTC'))
        )
        d2 = datetime.datetime(
            d1.datetime().year, d1.datetime().month, d1.datetime().day, 0, 0,
            0, tzinfo=timezone('UTC')
        )
        if d2.weekday() < 6:
            td = 6 - d2.weekday()
        else:
            td = 13 - d2.weekday()
        dr = d2 + datetime.timedelta(days=td)
        return dr

    def get_hw(self, year=datetime.datetime.now().year, nwd=[]):
        dr = self.get_dr(year)
        dr1 = dr + datetime.timedelta(days=-3)
        dr2 = dr + datetime.timedelta(days=-2)
        nwd.append(dr1.date())
        nwd.append(dr2.date())
        return nwd

    def get_carn(self, year=datetime.datetime.now().year, nwd=[]):
        dr = self.get_dr(year)
        dr1 = dr + datetime.timedelta(days=-48)
        dr2 = dr + datetime.timedelta(days=-47)
        nwd.append(dr1.date())
        nwd.append(dr2.date())
        return nwd
