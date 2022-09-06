from unittest import TestCase

from jota_utils.dict import getattr_nl, json_loads


class JsonLoadsTest(TestCase):

    def test_valid_json(self):
        self.assertEqual(json_loads('[1, 2, 3]'), [1, 2, 3])
        self.assertEqual(json_loads('[{"a": "b"}]'), [{'a': 'b'}])

    def test_invalid_json(self):
        self.assertEqual(json_loads('[1, 2, 3'), None)
        self.assertEqual(json_loads('[1, 2, 3', []), [])
        self.assertEqual(json_loads("['1']"), None)
        self.assertEqual(json_loads(None), None)


class GetAttrNlTest(TestCase):

    def test_with_obj_as_dict(self):
        obj = {'foo': {'bar': 'x'}}
        self.assertEqual(getattr_nl(obj, 'foo.bar'), 'x')

    def test_with_obj_as_instance(self):
        class TestObj:
            foo = 'bar'

        obj = TestObj()
        obj.new_foo = TestObj()
        self.assertEqual(getattr_nl(obj, 'foo'), 'bar')
        self.assertEqual(getattr_nl(obj, 'new_foo.foo'), 'bar')
        self.assertEqual(getattr_nl(obj, 'foo.inexisting_foo'), None)

    def test_with_invalid_objs(self):
        self.assertEqual(getattr_nl(None, 'a.b.c.d'), None)
        self.assertEqual(getattr_nl(None, 'a.b.c.d', default=[]), [])
        self.assertEqual(getattr_nl({}, 'a.b.c.d'), None)
        self.assertEqual(getattr_nl(False, 'a.b.c.d'), None)
