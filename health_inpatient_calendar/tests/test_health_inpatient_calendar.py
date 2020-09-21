from odoo.tests.common import TransactionCase

class HealthInpatientCalendarTestCase(TransactionCase):

    def set_up(self):
        super(HealthInpatientCalendarTestCase, self).setUp()
        self.model_obj = self.env['health.inpatient.calendar'].browse(1)
        self.assertFalse(
            self.model_obj.admitted(),
            self.model_obj.icu_stay(),
        )

