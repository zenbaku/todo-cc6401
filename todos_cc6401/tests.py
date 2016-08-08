from django.test import TestCase
from django.db import connection


class DBConnectionTestCase(TestCase):
    def setUp(self):
        self.cursor = connection.cursor()

    def test_connection(self):
        self.cursor.execute('SELECT 1')
        row = self.cursor.fetchone()
        self.assertEqual(row, (1,))


class AnimalTestCase(TestCase):
    def setUp(self):
        self.perro = True

    def test_basic_boolean_assert(self):
        self.assertEqual(self.perro, True)
