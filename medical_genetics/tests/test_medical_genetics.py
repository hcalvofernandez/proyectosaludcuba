# Copyright 2011-2020 GNU Solidario <medical@gnusolidario.org>
# Copyright 2020 LabViv
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo.tests.common import TransactionCase


class MedicalGeneticsTestCase(TransactionCase):

    def setUp(self, ):
        super(MedicalGeneticsTestCase, self).setUp()
        self.model_obj = self.env['medical.genetics']
        self.vals = {'name': 'Test Medical Genetics'}
