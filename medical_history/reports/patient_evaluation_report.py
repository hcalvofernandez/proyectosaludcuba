# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PatientEvaluation(models.AbstractModel):
    _name = 'report.medical_history.patient_evaluation'

    def get_marital_status(self, ids):
        this = self.env["medical.patient"].search([('id', '=', ids)])
        for record in this:
            if record.marital_status == 's':
                aux = 'Single'
            elif record.marital_status == 'm':
                aux = 'Married'
            elif record.marital_status == 'w':
                aux = 'Widow(er)'
            elif record.marital_status == 'd':
                aux = 'Divorced'
            else:
                aux = 'Separated'
        return aux

    def get_loc_eyes(self, ids):
        this = self.env["medical.patient.evaluation"].search([('id', '=', ids)])
        for record in this:
            if record.loc_eyes == '1':
                aux = 'Does not Open Eyes'
            elif record.loc_eyes == '2':
                aux = 'Opens eyes in response to painful stimuli'
            elif record.loc_eyes == '3':
                aux = 'Opens eyes in response to voice'
            else:
                aux = 'Opens eyes spontaneously'
        return aux

    def get_loc_verbal(self, ids):
        this = self.env["medical.patient.evaluation"].search([('id', '=', ids)])
        for record in this:
            if record.loc_verbal == '1':
                aux = 'Makes no sounds'
            elif record.loc_verbal == '2':
                aux = 'Incomprehensible sounds'
            elif record.loc_verbal == '3':
                aux = 'Utters inappropriate words'
            elif record.loc_verbal == '4':
                aux = 'Confused, disoriented'
            else:
                aux = 'Oriented, converses normally'
        return aux

    def get_loc_motor(self, ids):
        this = self.env["medical.patient.evaluation"].search([('id', '=', ids)])
        for record in this:
            if record.loc_motor == '1':
                aux = 'Makes no movement'
            elif record.loc_motor == '2':
                aux = 'Extension to painful stimuli - decerebrate response -'
            elif record.loc_motor == '3':
                aux = 'Abnormal flexion to painful stimuli (decorticate response)'
            elif record.loc_motor == '4':
                aux = 'Flexion / Withdrawal to painful stimuli'
            elif record.loc_motor == '5':
                aux = 'Localizes painful stimuli'
            else:
                aux = 'Obeys commands'
        return aux

    def get_discharge_reason(self, ids):
        this = self.env["medical.patient.evaluation"].search([('id', '=', ids)])
        for record in this:
            if record.discharge_reason == 'home':
                aux = 'Home / Selfcare'
            elif record.discharge_reason == 'transfer':
                aux = 'Transferred to another institution'
            else:
                aux = 'Death'
        return aux

    def get_xory(self, ids):
        this = self.env["medical.patient.family.diseases"].search([('patient', '=', ids)])
        for record in this:
            if record.xory == 'm':
                aux = 'Maternal'
            elif record.xory == 'f':
                aux = 'Paternal'
            elif record.xory == 's':
                aux = 'Sibling'
            else:
                aux = ''
        return aux

    def get_relative(self, ids):
        this = self.env["medical.patient.family.diseases"].search([('patient', '=', ids)])
        for record in this:
            if record.relative == 'mother':
                aux = 'Mother'
            elif record.relative == 'father':
                aux = 'Father'
            elif record.relative == 'brother':
                aux = 'Brother'
            elif record.relative == 'sister':
                aux = 'Sister'
            elif record.relative == 'aunt':
                aux = 'Aunt'
            elif record.relative == 'uncle':
                aux = 'Uncle'
            elif record.relative == 'nephew':
                aux = 'Nephew'
            elif record.relative == 'niece':
                aux = 'Niece'
            elif record.relative == 'grandfather':
                aux = 'Grandfather'
            elif record.relative == 'grandmother':
                aux = 'Grandmother'
            else:
                aux = 'Cousin'
        return aux

    def get_sexual_preferences(self, ids):
        this = self.env["medical.patient"].search([('id', '=', ids)])
        for record in this:
            if record.sexual_preferences == 'h':
                aux = 'Heterosexual'
            elif record.sexual_preferences == 'g':
                aux = 'Homosexual'
            elif record.sexual_preferences == 'b':
                aux = 'Bisexual'
            else:
                aux = 'Transexual'
        return aux

    @api.model
    def _get_report_values(self, docids, data=None):
        patient = self.env['medical.patient.evaluation'].browse(docids)
        return {
                'doc_ids': docids,
                'doc_model': 'medical.patient.evaluation',
                'docs': patient,
                'data': data,
                'marital_status': self.get_marital_status,
                'loc_eyes': self.get_loc_eyes,
                'loc_verbal': self.get_loc_verbal,
                'loc_motor': self.get_loc_motor,
                'discharge_reason': self.get_discharge_reason,
                'xory': self.get_xory,
                'relative': self.get_relative,
                'sexual_preferences': self.get_sexual_preferences,

               }
