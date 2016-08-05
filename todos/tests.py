from django.test import TestCase

class AnimalTestCase(TestCase):
    def setUp(self):
        self.perro = True

    def test_basic_boolean_assert(self):
        self.assertEqual(self.perro, False)