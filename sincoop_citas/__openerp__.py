# -*- coding: utf-8 -*-
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
