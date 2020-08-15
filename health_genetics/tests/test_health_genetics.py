# Copyright 2011-2020 GNU Solidario <health@gnusolidario.org>
# Copyright 2020 LabViv
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo.tests.common import TransactionCase


class HealthGeneticsTestCase(TransactionCase):

    def setUp(self, ):
        super(HealthGeneticsTestCase, self).setUp()
        self.model_obj = self.env['health.genetics']
        self.vals = {'name': 'Test Health Genetics'}
