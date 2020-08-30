from odoo.tests.common import TransactionCase
from datetime import  datetime

class TestInpatientIcu(TransactionCase):

    def set_up(self):
        super(TestInpatientIcu, self).setUp()
        self.model_obj = self.env['gnuhealth.inpatient.icu'].browse(1)
        self.assertFalse(
            self.model_obj.admitted(),
            self.model_obj.icu_stay(),
        )

    def test_icu_duration(self):
        """ Test returns nothing if no type """
        self.discharged_from_icu = False
        self.assertFalse(
            self.inpatient_1.icu_discharge_date(),
            self.inpatient_1.icu_stay(),
        )

