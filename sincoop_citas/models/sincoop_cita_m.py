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
#    Módulo Desarrollado por VeneSis-CPP (Asociación Cooperativa SIDIS).
#
###############################################################################

import calendar
from openerp import SUPERUSER_ID
from pytz import timezone
from openerp.osv import osv, fields
import datetime
from dateutil import easter, relativedelta, rrule
from openerp.addons.sincoop_citas.tools.cfg_timezone import Venezuelatz
from openerp.addons.sincoop_citas.tools.cfg_time_utils import TimeUtils


class sincoop_cita(osv.osv):
    _name = 'sincoop.cita'
    _description = u'Cita de una organización'
    _rec_name = 'fecha_cita'

    def _get_is_user_estado_cita(
        self, cr, uid, ids, field_name, arg, context=None
    ):
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = {}

        for taq in self.browse(cr, uid, ids):
            res[taq.id] = True
        return res

    def _search_is_user_estado_cita(self, cr, uid, obj, name, args, context):
        res_users = self.pool.get('res.users')
        res_users_data = res_users.browse(cr, uid, uid)[0]
        sincoop_cooperativa_obj = self.pool.get('sincoop.cooperativa')
        cooperativas_ids = sincoop_cooperativa_obj.search(
            cr, uid, [
                ('estado_id', '=', res_users_data.estado_id.id),
                ('create_uid', '!=', 1),
                ('state', '=', 'condo')
            ]
        )
        citas_ids = self.search(
            cr, uid, [('cooperativa_id', 'in', cooperativas_ids)]
        )
        return [('id', 'in', citas_ids)]

    _columns = {
        'is_user_estado_cita': fields.function(
            _get_is_user_estado_cita,
            method=True,
            string=u'¿Está el usuario en el mismo estado que la cooperativa \
            por cita?',
            type='boolean',
            fnct_search=_search_is_user_estado_cita
        ),
        'fecha_cita': fields.datetime(
            'Fecha y hora de la cita',
            readonly=False,
            required=False,
        ),
        'cooperativa_id': fields.many2one(
            'sincoop.cooperativa',
            u'Organización',
            help=u'Organización',
            required=True
        ),
        'taquilla_id': fields.many2one(
            'sincoop.taquilla.unica',
            'Oficina Regional',
            help=u'Oficina regional donde se realizará la cita',
            required=True
        ),
        'operador_id': fields.many2one(
            'res.users',
            u'Operador Oficina Regional'
        ),
        'state': fields.selection(
            [
                ('activa', 'Activa'),
                ('cancelada_por_taquilla', 'Cancelada por Oficina Regional'),
                ('noatendida', 'No atendida'),
                ('reasignada', 'Reasignacion'),
                ('completada', 'Completada'),
            ],
            string='Estatus',
            help=u"Estatus de la cita."
        ),
        'reasignada': fields.boolean(
            'Cita reasignada',
            help=u'Indica si la cita fue reasignada',
            default=False
        ),
    }

    def check_fecha_cita(
        self, cr, uid, fecha_cita, datos_taquilla, taquilla, rest, first_day,
        context=None
    ):
        vzlatz = Venezuelatz()
        hoy = datetime.datetime.now(vzlatz)
        td = fecha_cita.date() - hoy.date()
        fecha_n = datetime.datetime(
            fecha_cita.year, fecha_cita.month,
            fecha_cita.day, fecha_cita.hour,
            fecha_cita.minute, fecha_cita.second,
            tzinfo=vzlatz
        )
        if td.days <= 0:
            if rest:
                fecha_n = datetime.datetime(
                    hoy.year, hoy.month,
                    hoy.day, 9,
                    30, 0,
                    tzinfo=vzlatz
                ) + datetime.timedelta(days=2)
            else:
                fecha_n = datetime.datetime(
                    hoy.year, hoy.month,
                    hoy.day, 9,
                    30, 0,
                    tzinfo=vzlatz
                ) + datetime.timedelta(days=1)
        semana_final = datos_taquilla['fecha_final'].isocalendar()[1]
        semana = fecha_n.isocalendar()[1]
        if semana <= semana_final:
            if datos_taquilla['min_dia'] <= fecha_n.weekday() <= \
               datos_taquilla['max_dia']:
                if fecha_n.weekday() not in datos_taquilla['dias_laborables']:
                    for i in datos_taquilla['dias_laborables']:
                        if i > fecha_n.weekday():
                            difd = datetime.timedelta(
                                days=i - fecha_n.weekday()
                            )
                            fecha_n = fecha_n + difd
            elif datos_taquilla['min_dia'] > fecha_n.weekday():
                difd = datetime.timedelta(
                    days=datos_taquilla['min_dia'] - fecha_n.weekday()
                )
                fecha_n = fecha_n + difd
            else:
                diff_dias = (
                    6 - fecha_n.weekday() + datos_taquilla['min_dia']
                ) + 1
                delta = datetime.timedelta(days=diff_dias)
                fecha_n = fecha_n + delta
                if fecha_n.isocalendar()[1] <= semana_final:
                    pass
                else:
                    return False
        else:
            pass
        return fecha_n

    def add_months(self, date, months):
        month = date.month - 1 + months
        year = int(date.year + month / 12)
        month = month % 12 + 1
        day = min(date.day, calendar.monthrange(year, month)[1])
        return datetime.date(year, month, day)

    def obtener_taquilla(self, cr, uid, ids, context=None):
        if type(ids) == list:
            ids = ids[0]
        cooperativas = self.pool.get('sincoop.cooperativa')
        cooperativa_obj = cooperativas.browse(
            cr, uid, ids, context=None
        )
        for c in cooperativa_obj:
            codigo_estado = c.estado_id.id
        taquillas = self.pool.get('sincoop.taquilla.unica')
        taquilla_id = taquillas.search(
            cr, uid, [('estado_id', '=', codigo_estado)]
        )
        if taquilla_id:
            taquilla_obj = taquillas.browse(
                cr, uid, taquilla_id, context=None
            )[0]
            if taquilla_obj:
                return taquilla_obj
        return False

    def asignar_cita(
        self, cr, uid, ids, reasignada=False, rest=True, context=None
    ):
        cita_cancelada_id = []
        vzlatz = Venezuelatz()
        utctz = timezone('UTC')
        time_utils = TimeUtils()
        todayh = datetime.datetime.now(vzlatz)
        dia_nl = self.pool.get('sincoop.dia.no.laborable')
        taquillas = self.pool.get('sincoop.taquilla.unica')
        citas = self.pool.get('sincoop.cita')
        cooperativas = self.pool.get('sincoop.cooperativa')
        cooperativa = cooperativas.browse(cr, uid, ids)
        taquilla_relacionada = citas.obtener_taquilla(
            cr, uid, ids, context=None
        )
        today_plus_four = todayh + datetime.timedelta(days=2)

        if taquilla_relacionada:
            d1 = taquilla_relacionada.hora_inicio_jornada * 3600
            d2 = taquilla_relacionada.hora_fin_jornada * 3600
            intervalo_por_cita = datetime.timedelta(
                minutes=(taquilla_relacionada.intervalo_por_cita)
            )
            # Si existe una cita anterior y la misma es de actualización,
            # triplicar el intervalo:
            ultima_cita_id = citas.search(
                cr, uid, [
                    ('taquilla_id', '=', taquilla_relacionada.id),
                    ('state', '!=', 'cancelada_por_taquilla')
                ], order='fecha_cita desc', limit=1
            )
            if len(ultima_cita_id) > 0:
                if citas.browse(cr, SUPERUSER_ID, ultima_cita_id).\
                   cooperativa_id.migrada:
                    intervalo_por_cita *= 3
            almuerzo = datetime.timedelta(hours=1, minutes=30)
            intervalos = (d2 - d1 - almuerzo.seconds) /\
                intervalo_por_cita.seconds
            inicio_jornada = taquilla_relacionada.hora_inicio_jornada
            if len(ultima_cita_id) > 0:
                ultima_cita = citas.browse(
                    cr, uid, ultima_cita_id[0], context=context
                )
                ultima_cita_dict = time_utils.datestr2dict(
                    ultima_cita.fecha_cita
                )
                fecha_cita = time_utils.datedict2dt(
                    ultima_cita_dict, utctz
                )
                datos_taquilla = taquillas.get_taquillla_data(
                    cr, uid, int(fecha_cita.strftime("%Y")),
                    int(fecha_cita.strftime("%m")),
                    taquilla_relacionada.id
                )
            else:
                fecha_cita = datetime.datetime(
                    today_plus_four.year,
                    today_plus_four.month,
                    today_plus_four.day,
                    int(inicio_jornada),
                    int(inicio_jornada - int(inicio_jornada)) * 60,
                    tzinfo=vzlatz
                )
                datos_taquilla = taquillas.get_taquillla_data(
                    cr, uid, int(fecha_cita.strftime("%Y")),
                    int(fecha_cita.strftime("%m")),
                    taquilla_relacionada.id
                )
            if reasignada:
                fecha_cita_s = datetime.datetime(
                    todayh.year,
                    todayh.month,
                    todayh.day,
                    int(inicio_jornada),
                    int(inicio_jornada - int(inicio_jornada)) * 60,
                    tzinfo=vzlatz
                )
            else:
                fecha_cita_s = datetime.datetime(
                    datos_taquilla['fecha_inicial'].year,
                    datos_taquilla['fecha_inicial'].month,
                    datos_taquilla['fecha_inicial'].day,
                    int(inicio_jornada),
                    int(inicio_jornada - int(inicio_jornada)) * 60,
                    tzinfo=vzlatz
                )
            dday = 0
            if fecha_cita_s.weekday() <= datos_taquilla['min_dia']:
                dday = datos_taquilla['min_dia'] - fecha_cita_s.weekday()
            fecha_cita_i = fecha_cita_s + datetime.timedelta(days=dday)
            band = 1
            flag_max_citas = False
            while band:
                if flag_max_citas:
                    first_day = True
                    fecha_cita_plus_month = self.add_months(fecha_cita, 1)
                    datos_taquilla = taquillas.get_taquillla_data(
                        cr, uid, int(fecha_cita_plus_month.year),
                        str(fecha_cita_plus_month.month),
                        taquilla_relacionada.id
                    )
                    fecha_cita_s = datetime.datetime(
                        datos_taquilla['fecha_inicial'].year,
                        datos_taquilla['fecha_inicial'].month,
                        datos_taquilla['fecha_inicial'].day,
                        int(inicio_jornada),
                        int(inicio_jornada - int(inicio_jornada)) * 60,
                        tzinfo=vzlatz
                    )
                    fecha_cita = citas.check_fecha_cita(
                        cr, uid, fecha_cita_s, datos_taquilla,
                        taquilla_relacionada, rest, first_day, context
                    )
                else:
                    first_day = False
                    fecha_cita = citas.check_fecha_cita(
                        cr, uid, fecha_cita_i, datos_taquilla,
                        taquilla_relacionada, rest, first_day, context
                    )
                if not fecha_cita:
                    if today_plus_four.month > todayh.month:
                        datos_taquilla = taquillas.get_taquillla_data(
                            cr, uid, int(today_plus_four.year),
                            str(today_plus_four.month),
                            taquilla_relacionada.id
                        )
                        fecha_cita_s = datetime.datetime(
                            datos_taquilla['fecha_inicial'].year,
                            datos_taquilla['fecha_inicial'].month,
                            datos_taquilla['fecha_inicial'].day,
                            int(inicio_jornada),
                            int(inicio_jornada - int(inicio_jornada)) * 60,
                            tzinfo=vzlatz
                        )
                        fecha_cita = citas.check_fecha_cita(
                            cr, uid, fecha_cita_s, datos_taquilla,
                            taquilla_relacionada, rest, first_day, context
                        )
                    res = {
                        'flag': False,
                        'msg': u'Su solicitud no ha podido ser procesada, por\
                        favor inténtelo de nuevo. Si persiste este error,\
                        contacte a Soporte Técnico.'
                    }

                citas_taquilla = citas.search(
                    cr, uid, [
                        (
                            'fecha_cita', '>=',
                            datos_taquilla['fecha_inicial'].astimezone(
                                utctz
                            ).strftime("%Y-%m-%d %H:%M:%S")
                        ),
                        (
                            'taquilla_id', '=', taquilla_relacionada.id
                        ),
                        ('state', '=', 'activa'),
                    ], count=True
                )
                if citas_taquilla:
                    cita_cooperativa = citas.search(
                        cr, uid, [
                            (
                                'state', 'in', [
                                    'completada', 'activa'
                                ]
                            ),
                            ('reasignada', '=', False),
                            ('cooperativa_id', '=', cooperativa.id),
                        ], order='id', count=True
                    )
                    if cita_cooperativa:
                        res = {
                            'flag': False,
                            'msg': 'La cooperativa tiene una cita previa.\
                            No puede solicitar una nueva cita.'
                        }
                    else:
                        try:
                            citas_canceladas = citas.search(
                                cr, uid, [
                                    (
                                        'fecha_cita', '>=',
                                        fecha_cita.astimezone(utctz).strftime(
                                            "%Y-%m-%d %H:%M:%S"
                                        )
                                    ),
                                    (
                                        'taquilla_id',
                                        '=',
                                        taquilla_relacionada.id
                                    ),
                                    ('state', '!=', 'activa'),
                                    ('state', '!=', 'completada'),
                                    ('state', '!=', 'noatendida'),
                                    ('state', '!=', 'reasignada'),
                                    ('reasignada', '=', False)
                                ], order='id', count=True
                            )
                        except:
                            citas_canceladas = []
                        if citas_canceladas:
                            cita_cancelada_id = citas.search(
                                cr, uid, [
                                    (
                                        'fecha_cita', '>=',
                                        fecha_cita.astimezone(utctz).strftime(
                                            "%Y-%m-%d %H:%M:%S"
                                        )
                                    ),
                                    (
                                        'taquilla_id', '=',
                                        taquilla_relacionada.id
                                    ),
                                    ('state', '!=', 'activa'),
                                    ('state', '!=', 'completada'),
                                    ('state', '!=', 'noatendida'),
                                    ('state', '!=', 'reasignada'),
                                    ('reasignada', '=', False)
                                ], order='id'
                            )
                            cita_cancelada = citas.browse(
                                cr, uid, cita_cancelada_id[0]
                            )
                            dia_cita_cancelada_dic = time_utils.datestr2dict(
                                cita_cancelada.date
                            )
                            fecha_cita = time_utils.datedict2dt(
                                dia_cita_cancelada_dic, utctz
                            )
                            res = {
                                'flag': True,
                                'msg': u'¡Felicidades! Se ha generado una cita\
                                de verificación para su cooperativa. En su\
                                buzón de correo electrónico tiene detalles de\
                                la cita.'
                            }
                        else:
                            ultima_cita_id = citas.search(
                                cr, uid, [
                                    (
                                        'taquilla_id', '=',
                                        taquilla_relacionada.id
                                    ),
                                    (
                                        'state', '!=',
                                        'cancelada_por_taquilla'
                                    )
                                ], order='fecha_cita desc', limit=1
                            )
                            ultima_cita = citas.browse(
                                cr, uid, ultima_cita_id[0], context=context
                            )
                            ultima_cita_dict = time_utils.datestr2dict(
                                ultima_cita.fecha_cita
                            )
                            fecha_cita_aux = time_utils.datedict2dt(
                                ultima_cita_dict, utctz
                            )
                            if fecha_cita <= fecha_cita_aux:
                                fecha_cita = fecha_cita_aux
                            fecha_cita_count = citas.search(
                                cr, uid, [
                                    (
                                        'fecha_cita', '=',
                                        fecha_cita.strftime(
                                            "%Y-%m-%d %H:%M:%S"
                                        )
                                    ),
                                    (
                                        'taquilla_id', '=',
                                        taquilla_relacionada.id
                                    ),
                                    (
                                        'state', '!=',
                                        'cancelada_por_taquilla'
                                    )
                                ], count=True
                            )
                            if fecha_cita_count < int(
                               taquilla_relacionada.max_citas_por_intervalo
                               ):
                                band = 0
                                flag_max_citas = False
                                res = {
                                    'flag': True,
                                    'msg': u'¡Felicidades! Se ha generado una\
                                    cita de verificación para su cooperativa.\
                                    En su buzón de correo electrónico tiene\
                                    detalles de la cita.'
                                }
                            else:
                                d5 = datetime.timedelta(
                                    hours=fecha_cita.astimezone(
                                        vzlatz
                                    ).hour,
                                    minutes=fecha_cita.astimezone(
                                        vzlatz
                                    ).minute
                                )
                                tiempo_intervalo = (
                                    d5.seconds - d1 -
                                    almuerzo.seconds
                                ) / intervalo_por_cita.seconds
                                if tiempo_intervalo < (intervalos - 1):
                                    if fecha_cita.astimezone(vzlatz).hour \
                                       == 11 and fecha_cita.\
                                       astimezone(vzlatz).minute == 30:
                                        fecha_cita = fecha_cita + almuerzo
                                    else:
                                        fecha_cita = fecha_cita + \
                                            intervalo_por_cita
                                    res = {
                                        'flag': True,
                                        'msg': u'¡Felicidades! Se ha generado\
                                        una cita de verificación para su\
                                        cooperativa. En su buzón de correo\
                                        electrónico tiene detalles de la cita.'
                                    }
                                else:
                                    if fecha_cita.astimezone(vzlatz).\
                                       weekday() < \
                                       datos_taquilla['max_dia']:
                                        pos = datos_taquilla[
                                            'dias_laborables'
                                        ].index(fecha_cita.astimezone(
                                            vzlatz
                                        ).weekday())
                                        dia = datos_taquilla[
                                            'dias_laborables'
                                        ][pos + 1]
                                        delta = datetime.timedelta(
                                            days=dia - fecha_cita.astimezone(
                                                vzlatz
                                            ).weekday()
                                        )
                                        dia_aux = fecha_cita.astimezone(
                                            vzlatz
                                        ) + delta
                                        fecha_cita = datetime.datetime(
                                            dia_aux.year,
                                            dia_aux.month,
                                            dia_aux.day,
                                            int(inicio_jornada),
                                            int(inicio_jornada -
                                            int(inicio_jornada)) * 60,
                                            tzinfo=vzlatz
                                        )
                                        res = {
                                            'flag': True,
                                            'msg': u'¡Felicidades! Se ha \
                                            generado una cita de verificación\
                                            para su cooperativa. En su buzón\
                                            de correo electrónico tiene\
                                            detalles de la cita.'
                                        }
                                    else:
                                        fin_semana = datos_taquilla[
                                            'fecha_final'
                                        ].isocalendar()[1]
                                        semana = fecha_cita.astimezone(
                                            vzlatz
                                        ).isocalendar()[1]
                                        if semana < fin_semana:
                                            diff_dias = (
                                                6 - datos_taquilla[
                                                    'max_dia'
                                                ] + datos_taquilla[
                                                    'min_dia'
                                                ]
                                            ) + 1
                                            delta = datetime.timedelta(
                                                days=diff_dias
                                            )
                                            dia_aux = fecha_cita.\
                                                astimezone(vzlatz) + delta
                                            fecha_cita = datetime.datetime(
                                                dia_aux.year,
                                                dia_aux.month, dia_aux.day,
                                                int(inicio_jornada),
                                                int(
                                                    inicio_jornada -
                                                    int(inicio_jornada)
                                                ) * 60,
                                                tzinfo=vzlatz
                                            )
                                            flag_max_citas = False
                                            res = {
                                                'flag': True,
                                                'msg': u'¡Felicidades! Se ha\
                                                generado una cita de\
                                                verificación para su\
                                                cooperativa. En su buzón de\
                                                correo electrónico tiene\
                                                detalles de la cita.'
                                            }
                                        else:
                                            flag_max_citas = True
                                            band = 1
                                            res = {}
                                            res['flag'] = False
                            if not flag_max_citas:
                                band = 0
                                flag_max_citas = False
                                res = {
                                    'flag': True,
                                    'msg': u'¡Felicidades! Se ha generado una\
                                    cita de verificación para su cooperativa.\
                                    En su buzón de correo electrónico tiene\
                                    detalles de la cita.'
                                }
                else:
                    flag_max_citas = False
                    res = {
                        'flag': True,
                        'msg': u'¡Felicidades! Se ha generado una cita de\
                        verificación para su cooperativa. En su buzón de\
                        correo electrónico tiene detalles de la cita.'
                    }
                if res['flag']:
                    # Verificar que el día asignado sea laborable
                    dia_nl_obj = self.pool.\
                        get('sincoop.dia.no.laborable')
                    dia_nl = dia_nl_obj.\
                        search(cr, uid, [('fecha', '=', fecha_cita)])
                    if dia_nl:
                        # El día no es laborable:
                        fecha_cita_i = fecha_cita + datetime.timedelta(days=1)
                        band = 1
                        flag_max_citas = False
                    else:
                        # El día es laborable:
                        band = 0
                        flag_max_citas = False
                if flag_max_citas and band != 1:
                    band = 1
        else:
            res = {
                'flag': False,
                'msg': u'No se ha podido designar Oficina Regional para su\
                cita.'
            }
        if res['flag']:
            if fecha_cita.tzname() == 'UTC':
                datetz = fecha_cita
            else:
                datetz = fecha_cita.astimezone(utctz)
            try:
                if cita_cancelada_id:
                    citas.write(
                        cr, uid, cita_cancelada_id[0], {'reasignada': True}
                    )
                else:
                    citas.create(
                        cr, uid, {
                            'fecha_cita': datetz,
                            'cooperativa_id': cooperativa.id,
                            'state': 'activa',
                            'taquilla_id': taquilla_relacionada.id,
                        }
                    )
            except (osv.except_osv, ValueError):
                raise
        return res


class sincoop_dia_no_laborable(osv.Model):
    """
    Clase para almacenar los días no laborables para cada Oficina Regional.
    El modelo de citas verifica que el día no esté marcado aquí para la Oficina
    Regional que atenderá la respectiva cita.
    Incluye de manera predeterminada sábados, domingos y feriados por Ley.
    """
    _name = "sincoop.dia.no.laborable"
    _description = u"Días no laborables"
    _columns = {
        'fecha': fields.date('Fecha', required=False),
        'name': fields.char(u'Nombre del día', size=64, required=True),
        'dia': fields.integer(u'Número de día', required=True),
        'mes': fields.integer(u'Número de mes', required=True),
        'tipo': fields.selection(
            (
                ('lot', 'LOTTT'),
                ('lfn', 'Ley de Fiestas Nacionales'),
                ('dec', 'Otra Ley o Decreto de efecto nacional'),
                ('reg', 'Decreto Regional'),
                ('mun', 'Ordenanza Municipal'),
                ('con', 'Contingencia')
            ),
            'Tipo de dia no laborable',
            required=True
        ),
        'taquilla_id': fields.many2many(
            'sincoop.taquilla.unica',
            'rel_dia_oficina_reg',
            'taquilla_id',
            'dia_id',
            u'Oficina Regional afectada',
        ),
        'gencal': fields.selection(
            (
                ('gen', 'Genérico'),
                ('cal', 'Calculado')
            ),
            'Tipo de registro',
            required=True
        ),
        'activo': fields.boolean('Activo')
    }

    def inicializar(self, cr, uid, ids, context=None):
        year = datetime.datetime.now().year
        before = datetime.datetime(year, 1, 1)
        after = datetime.datetime(year, 12, 31)
        registro = self.browse(cr, uid, ids)
        # Generar una lista con los IDs de las taquillas, para poder
        # inyectarlas en el many2many:
        taquillas = registro.taquilla_id
        taq_ids = []
        for taquilla in taquillas:
            taq_ids.append(taquilla.id)

        # Registrar domingos si estan marcados en la data, al igual que los
        # demás días con fechas fijas.
        if registro.name == "Domingos" and registro.activo:
            rr = rrule.rrule(
                rrule.WEEKLY, byweekday=relativedelta.SU, dtstart=before
            )
            for dia in rr.between(before, after, inc=True):
                dia = datetime.date(dia.year, dia.month, dia.day)
                if not self.search(cr, uid, [('fecha', '=', dia)]):
                    self.create(cr, uid, {
                        'fecha': dia,
                        'name': "Dom. " + str(dia.day) + "/" + str(dia.month),
                        'dia': dia.day,
                        'mes': dia.month,
                        'tipo': registro.tipo,
                        'taquilla_id': [(6, 0, taq_ids)],  # ¡Magia!
                        'gencal': 'cal',
                        'activo': True
                    })
            otros_ids = self.search(
                cr, uid, [
                    (
                        'name', 'not in', [
                            'Domingos', 'Sábados', 'Lunes de carnaval',
                            'Martes de carnaval', 'Jueves santo',
                            'Viernes santo'
                        ]
                    ),
                    ('gencal', '=', 'cal'),
                    ('activo', '=', True)
                ]
            )
            otros = self.browse(cr, uid, otros_ids)
            for dia in otros:
                fecha = datetime.date(year, dia.mes, dia.dia)
                if not self.search(cr, uid, [('fecha', '=', fecha)]):
                    self.create(cr, uid, {
                        'fecha': fecha,
                        'name': dia.name,
                        'dia': dia.dia,
                        'mes': dia.mes,
                        'tipo': registro.tipo,
                        'taquilla_id': [(6, 0, taq_ids)],  # ¡Magia!
                        'gencal': 'cal',
                        'activo': True
                    })

        # Registrar sábados si estan marcados en la data.
        elif registro.name == u"Sábados" and registro.activo:
            rr = rrule.rrule(
                rrule.WEEKLY, byweekday=relativedelta.SA, dtstart=before
            )
            for dia in rr.between(before, after, inc=True):
                dia = datetime.date(dia.year, dia.month, dia.day)
                if not self.search(cr, uid, [('fecha', '=', dia)]):
                    self.create(cr, uid, {
                        'fecha': dia,
                        'name': "Sáb. " + str(dia.day) + "/" + str(dia.month),
                        'dia': dia.day,
                        'mes': dia.month,
                        'tipo': registro.tipo,
                        'taquilla_id': [(6, 0, taq_ids)],  # ¡Magia!
                        'gencal': 'cal',
                        'activo': True
                    })

        # Registrar semana santa. Método utilizado por la iglesia católica:
        # Buscar el primer domingo de la primera luna llena a partir de la
        # primavera (equinoccio) = Domingo de pascua o Domingo de Resurrección.
        elif registro.name == 'Carnaval y Semana Santa' and registro.activo:
            dom_res = str(easter.easter(year)).split("-")
            dom_res = datetime.date(
                int(dom_res[0]), int(dom_res[1]), int(dom_res[2])
            )
            lun_car = dom_res + datetime.timedelta(days=-41)
            mar_car = dom_res + datetime.timedelta(days=-40)
            jue_san = dom_res + datetime.timedelta(days=-3)
            vie_san = dom_res + datetime.timedelta(days=-2)
            carysemsan = [lun_car, mar_car, jue_san, vie_san]
            contador = 0
            for dia in carysemsan:
                contador += 1
                if contador == 1:
                    descr = "Lunes de carnaval"
                elif contador == 2:
                    descr = "Martes de carnaval"
                elif contador == 3:
                    descr = "Jueves santo"
                else:
                    descr = "Viernes santo"
                self.create(cr, uid, {
                    'fecha': dia,
                    'name': descr,
                    'dia': dia.day,
                    'mes': dia.month,
                    'tipo': registro.tipo,
                    'taquilla_id': [(6, 0, taq_ids)],  # ¡Magia!
                    'gencal': 'cal',
                    'activo': True
                })

        return
