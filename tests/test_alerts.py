import unittest
from hydropulse.alerts.controller import AlertController
class TestAlert(unittest.TestCase):
    def test_a(self):
        a = AlertController().evaluate_alert(1.10, 0.8, 1.4, 92)
        self.assertEqual(a['alert_level'], 'CRITICAL_MAJOR_FLOOD')
