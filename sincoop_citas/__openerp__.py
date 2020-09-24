# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Módulo Desarrollado por VeneSis-CPP (Asociaciones Cooperativa SIDIS).
#
###############################################################################
{
    'name': "SINCOOP Citas - Sistema de Gestión Integrado para las\
    Cooperativas y Organismos de Integración",
    'summary': "",
    'description': u"Módulo para la asignación de citas.",
    'author': "VeneSis-CCP (SIDIS) / CPUi",
    'category': "SINCOOP",
    'version': '1.0',
    'depends': ['base', 'sincoop_cooperativa', 'sincoop_taquilla_unica'],
    'data': [
        "security/sincoop_dia/group_asociado/ir.model.access.csv",
        "security/sincoop_dia_no_laborable/group_asociado/ir.model.access.csv",
        "security/sincoop_cita/group_asociado/ir.model.access.csv",
        "security/sincoop_cita/group_coordinador_taquilla/ir.model.access.csv",
        "security/sincoop_cita/group_operador_soporte/ir.model.access.csv",
        "security/sincoop_dia/group_operador_taquilla/ir.model.access.csv",
        "data/sincoop.dia.no.laborable.csv",
        "views/sincoop_dia_no_laborable_v.xml"
    ],
    'demo': [],
    'tests': [],
    'installable': True,
    'auto_install': False,
}
