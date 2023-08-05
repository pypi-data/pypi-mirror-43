from enum import auto
from unittest import TestCase
from serflag import SerFlag


class TestSerFlag(TestCase):
    def setUp(self):
        class TestClass(SerFlag):
            Red = auto()
            Blue = auto()
            Black = auto()

        self.TestClass = TestClass

    def test_all_in_class(self):
        self.assertTrue(hasattr(self.TestClass, 'ALL'))

    def test_serialize_all(self):
        serialized = self.TestClass.ALL.serialize()
        self.assertEqual(['ALL'], serialized, "serialize(['ALL']) should return ALL")

    def test_serialize_none(self):
        self.assertEqual([], self.TestClass.NONE.serialize())

    def test_serialize_some(self):
        self.assertCountEqual(['Black', 'Red'], (self.TestClass.Black | self.TestClass.Red).serialize())

    def test_serialize_one(self):
        self.assertEqual(['Blue'], self.TestClass.Blue.serialize())

    def test_serialize_every(self):
        self.assertCountEqual(['Black', 'Red', 'Blue'], (self.TestClass.Black | self.TestClass.Red | self.TestClass.Blue).serialize())

    def test_all_not_in_enum_with_every_value(self):
        enum_with_every_value = self.TestClass.Red | self.TestClass.Blue | self.TestClass.Black
        self.assertNotIn(self.TestClass.ALL, enum_with_every_value, "ALL should not be in enum with every possible value except ALL")

    def test_enum_with_every_value_in_all(self):
        enum_with_every_value = self.TestClass.Red | self.TestClass.Blue | self.TestClass.Black
        self.assertIn(enum_with_every_value, self.TestClass.ALL, "Every enum value should be in ALL")

    def test_deserialize(self):
        self.assertEqual(self.TestClass.Red, self.TestClass.deserialize(['Red']))
        self.assertEqual(self.TestClass.Blue, self.TestClass.deserialize(['Blue']))
        self.assertEqual(self.TestClass.Black, self.TestClass.deserialize(['Black']))

    def test_deserialize_composite(self):
        self.assertEqual(self.TestClass.Red | self.TestClass.Black,
                         self.TestClass.deserialize(['Red', 'Black']))

    def test_deserialize_all(self):
        self.assertEqual(self.TestClass.ALL, self.TestClass.deserialize(['ALL']))

    def test_deserialize_distinct(self):
        self.assertEqual([self.TestClass.Red], self.TestClass.deserialize_distinct(['Red']))
        self.assertEqual([self.TestClass.Blue], self.TestClass.deserialize_distinct(['Blue']))
        self.assertEqual([self.TestClass.Black], self.TestClass.deserialize_distinct(['Black']))

    def test_deserialize_distinct_composite(self):
        self.assertCountEqual([self.TestClass.Red, self.TestClass.Black],
                         self.TestClass.deserialize_distinct(['Red', 'Black']))

    def test_deserialize_distinct_all(self):
        self.assertCountEqual([self.TestClass.Red, self.TestClass.Black, self.TestClass.Blue],
                         self.TestClass.deserialize_distinct(['ALL']))










