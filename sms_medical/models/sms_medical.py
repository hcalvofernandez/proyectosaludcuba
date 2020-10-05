# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import sys
from ..rsgv1 import RESTSMSGateway

API_URL = 'http://localhost'

class SmsMedical(models.Model):
    _name = "sms.medical"
    _description = "SMS/Medical GNU"
    _order = "id desc"
    _inherit = ['format.address.mixin', 'phone.validation.mixin']

    phone = fields.Char('')
    event_name = fields.Char('',default="Medical sms")#Llenar el nombre del evento que llama al sms
    message = fields.Text('')
    state = fields.Selection([('draft','draft'),('send','send'),('cancel','cancel')])

    @api.model
    def get_next_case(self):  # TODO cambiar para adaptar a las citas de medical
        """ Cron method, overridden here to send SMS reminders as well
        """
        result = super(SmsMedical, self).get_next_case()
        now = fields.Datetime.to_string(fields.Datetime.now())
        last_sms_cron = self.env['ir.config_parameter'].get_param('calendar_sms_medical.last_sms_medical_cron', default=now)
        cron = self.env['ir.model.data'].get_object('calendar', 'ir_cron_scheduler_alarm')

        interval_to_second = {
            "weeks": 7 * 24 * 60 * 60,
            "days": 24 * 60 * 60,
            "hours": 60 * 60,
            "minutes": 60,
            "seconds": 1
        }

        cron_interval = cron.interval_number * interval_to_second[cron.interval_type]
        events_data = self._get_next_potential_limit_alarm('sms', seconds=cron_interval)  # TODO check type of events

        for event in self.env['calendar.event'].browse(events_data):
            max_delta = events_data[event.id]['max_duration']

            if event.recurrency:
                found = False
                for event_start in event._get_recurrent_date_by_event():
                    event_start = event_start.replace(tzinfo=None)
                    last_found = self.do_check_alarm_for_one_date(event_start, event, max_delta, 0, 'sms',
                                                                  after=last_sms_cron, missing=True)
                    for alert in last_found:
                        event.browse(alert['event_id'])._do_sms_reminder()
                        found = True
                    if found and not last_found:  # if the precedent event had an alarm but not this one, we can stop the search for this event
                        break
            else:
                event_start = fields.Datetime.from_string(event.start)
                for alert in self.do_check_alarm_for_one_date(event_start, event, max_delta, 0, 'sms',
                                                              after=last_sms_cron, missing=True):
                    event.browse(alert['event_id'])._do_sms_reminder()
        self.env['ir.config_parameter'].set_param('calendar_sms_medical.last_sms_medical_cron', now)
        return result


    def send_sms(self):
        self._envio_simple(self.phone,self.message,'default-sms')

    def _envio_simple(self,phone,message,event_name):#envio simple
        r = RESTSMSGateway(API_URL, '8080')
        r.sendSMS(phone,message)
        self.env['sms.medical'].create({
            'phone':phone,
            'event_name':   event_name,
            'message':   message,
            'state':   'send',
        })


    def envio_masivo(self,contacts,message):
        if contacts:
            for phone in contacts:
                self._envio_simple(phone,message)


    def almacenar(self):
        r = RESTSMSGateway(sys.argv[1], '8080', debug=False)
        mensajes = r.getSMSAll(limit=1000)['messages']
        for mensaje in reversed(mensajes):
            mensaje_id = int(mensaje["_id"])
            sms = r.getSMSById(mensaje_id, )["sms"][0]
            if sms["msg_box"] == 'inbox':
                print(
                    sms["msg_box"] + "|" + sms["_id"] + "|" +
                    sms["address"] + "|" + sms["body"]
                )

    def _sms_get_number_fields(self):
        """ This method returns the fields to use to find the number to use to
        send an SMS on a record. """
        return ['mobile', 'phone']
