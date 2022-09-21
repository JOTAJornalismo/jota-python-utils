from unittest import TestCase

from jota_utils.dict import getattr_nl, json_loads, with_except, with_only


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
        self.assertEqual(getattr_nl({'e': 'x'}, 'a.b.c.d'), None)
        self.assertEqual(getattr_nl(False, 'a.b.c.d'), None)


class ExceptOnlyTest(TestCase):
    TEST_DICT = {'a': 1, 'b': 2, 'c': 3}

    def test_with_except(self):
        self.assertEqual(with_except(self.TEST_DICT.copy(), ['b', 'c']), {'a': 1})
        self.assertEqual(with_except({}, ['b', 'c']), {})
        self.assertEqual(with_except(self.TEST_DICT.copy(), []), self.TEST_DICT.copy())
        self.assertEqual(with_except({}, []), {})

    def test_with_only(self):
        self.assertEqual(with_only(self.TEST_DICT.copy(), ['b', 'c']), {'b': 2, 'c': 3})
        self.assertEqual(with_only({}, ['b', 'c']), {})
        self.assertEqual(with_only(self.TEST_DICT.copy(), []), {})
        self.assertEqual(with_only({}, []), {})
