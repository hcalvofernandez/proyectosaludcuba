# -*- coding: utf-8 -*-

__all__ = ['HospitalBed', 'InpatientRegistration']

from odoo import api, fields, models, _


class HospitalBed(models.Model):
    "Add Calendar to Hospital Bed"
    _inherit = "medical.hospital.bed"

    calendar = fields.Many2one('calendar.event', 'Calendar')


class InpatientRegistration(models.Model):
    'Add Calendar to the Inpatient Registration'
    _inherit = 'medical.inpatient.registration'

    event = fields.Many2one('calendar.event', 'Calendar Event', readonly=True,
        help="Calendar Event")

    def confirmed(self, registrations):
        super(InpatientRegistration, self).confirmed(registrations)

        Event = self.env.get('calendar.event')

        for inpatient_registration in registrations:
            if inpatient_registration.bed.calendar:
                if not inpatient_registration.event:
                    bed = inpatient_registration.bed.name.code + ": "
                    events = Event.create([{
                        'dtstart': inpatient_registration.hospitalization_date,
                        'dtend': inpatient_registration.discharge_date,
                        'calendar': inpatient_registration.bed.calendar.id,
                        'summary': bed + inpatient_registration.patient.name.rec_name
                        }])
                    self.write([inpatient_registration],
                        {'event': events[0].id})

    @classmethod
    def discharge(self, registrations):
        super(InpatientRegistration, self).discharge(registrations)

        Event = self.env.get('calendar.event')

        for inpatient_registration in registrations:
            if inpatient_registration.event:
                Event.delete([inpatient_registration.event])

    @classmethod
    def write(self, registrations, values):
        Event = self.env.get('calendar.event')
        Patient = self.env.get('gnuhealth.patient')
        HospitalBed = self.env.get('gnuhealth.hospital.bed')

        for inpatient_registration in registrations:
            if inpatient_registration.event:
                if 'hospitalization_date' in values:
                    Event.write([inpatient_registration.event], {
                        'dtstart': values['hospitalization_date'],
                        })
                if 'discharge_date' in values:
                    Event.write([inpatient_registration.event], {
                        'dtend': values['discharge_date'],
                        })
                if 'bed' in values:
                    bed = HospitalBed(values['bed'])
                    Event.write([inpatient_registration.event], {
                        'calendar': bed.calendar.id,
                        })
                if 'patient' in values:
                    patient = Patient(values['patient'])
                    bed = inpatient_registration.bed.name.code + ": "
                    Event.write([inpatient_registration.event], {
                        'summary': bed + patient.name.rec_name,
                        })

        return super(InpatientRegistration, self).write(registrations, values)

    @classmethod
    def delete(self, registrations):
        Event = self.env.get('calendar.event')

        for inpatient_registration in registrations:
            if inpatient_registration.event:
                Event.delete([inpatient_registration.event])
        return super(InpatientRegistration, self).delete(registrations)
