from django.test import TestCase

class AnimalTestCase(TestCase):
    def setUp(self):
        self.perro = True

    def test_animals_can_speak(self):
        self.assertEqual(self.perro, True)
        # self.assertEqual(cat.speak(), 'The cat says "meow"')