from unittest import TestCase


from jota_utils.dict import (find_first_in_dict_list, find_in_dict_list,
                             getattr_nl, json_loads, with_except, with_only,
                             duplicates, remove_duplicates, pluck, is_superset,
                             setattrs)

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
        obj.new_foo = TestObj() # type: ignore 
        self.assertEqual(getattr_nl(obj, 'foo'), 'bar')
        self.assertEqual(getattr_nl(obj, 'new_foo.foo'), 'bar')
        self.assertEqual(getattr_nl(obj, 'foo.inexisting_foo'), None)

    def test_with_obj_as_instance_with_dict(self):
        class TestObj:
            foo = {'bar': {'param': 'a'}}

        obj = TestObj()

        self.assertEqual(getattr_nl(obj, 'foo.bar'), {'param': 'a'})
        self.assertEqual(getattr_nl(obj, 'foo.bar.param'), 'a')
        self.assertEqual(getattr_nl(obj, 'foo.bar.inexisting_foo'), None)

    def test_with_invalid_objs(self):
        self.assertEqual(getattr_nl(None, 'a.b.c.d'), None)
        self.assertEqual(getattr_nl(None, 'a.b.c.d', default=[]), [])
        self.assertEqual(getattr_nl({}, 'a.b.c.d'), None)
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


class FindInDictListTest(TestCase):

    def test_find_in_dict_list(self):
        data = [{'fruit': 'orange'}, {'fruit': 'apple'}, {'fruit': 'orange'}]

        self.assertEqual(
            find_in_dict_list('fruit', 'orange', data),
            [{'fruit': 'orange'}, {'fruit': 'orange'}]
        )
        self.assertEqual(find_in_dict_list('inexisting_key', 'orange', data), [])
        self.assertEqual(find_in_dict_list('fruit', 'orange', []), [])

    def test_find_first_in_dict_list(self):
        data = [{'fruit': 'orange'}, {'fruit': 'apple'}, {'fruit': 'orange'}]

        self.assertEqual(find_first_in_dict_list('fruit', 'orange', data), {'fruit': 'orange'})
        self.assertEqual(find_first_in_dict_list('fruit', 'lemon', data), None)


class DuplicatesTest(TestCase):

    def test_duplicates(self):
        data = [{'fruit': 'orange'}, {'fruit': 'apple'}, {'fruit': 'orange'}]

        self.assertEqual(duplicates('fruit', data), ['orange'])
        self.assertEqual(duplicates('fruit', []), [])
        self.assertEqual(duplicates('fruit', [{'fruit': 'apple'}, {'fruit': 'orange'}]), [])

    def test_remove_duplicates(self):
        data = [
            {'id': 1, 'fruit': 'orange'},
            {'id': 2, 'fruit': 'apple'},
            {'id': 3, 'fruit': 'orange'},
            {'id': 4, 'fruit': 'apple'}
        ]
        remove_duplicates('fruit', data)
        self.assertEqual(data, [{'id': 3, 'fruit': 'orange'}, {'id': 4, 'fruit': 'apple'}])

        data = []
        remove_duplicates('fruit', data)
        self.assertEqual(data, [])

        data = [{'fruit': 'apple'}, {'fruit': 'orange'}]
        remove_duplicates('fruit', data)
        self.assertEqual(data, [{'fruit': 'apple'}, {'fruit': 'orange'}])


class PluckTest(TestCase):

    def test_pluck(self):
        self.assertEqual(pluck('value', [{'value': 1}, {'value': 2}]), [1, 2])
        self.assertEqual(pluck('value', []), [])

    def test_pluck_with_dot_notation(self):
        class TestObj:
            foo = {'bar': {'param': 'a'}}

        obj_a = TestObj()

        obj_b = TestObj()
        obj_b.foo = {'bar': {'param': 'b'}}

        self.assertEqual(pluck('foo.bar.param', [obj_a, obj_b]), ['a', 'b'])

class IsSupersetTest(TestCase):

    def test_is_superset_true(self):
        dict_a = {'a': 1, 'b': 2, 'c': 3}
        dict_b = {'a': 1, 'b': 2}
        self.assertTrue(is_superset(dict_a, dict_b))        

    def test_is_superset_false(self):
        dict_a = {'a': 1, 'b': 2}
        dict_b = {'a': 1, 'b': 2, 'c': 3}
        self.assertFalse(is_superset(dict_a, dict_b))
        self.assertFalse(is_superset({'a':1},None))

    def test_is_superset_with_empty_dicts(self):
        self.assertTrue(is_superset({}, {}))
        self.assertFalse(is_superset({}, {'a': 1}))

    def test_is_superset_with_different_values(self):
        dict_a = {'a': 1, 'b': 2}
        dict_b = {'a': 2}
        self.assertFalse(is_superset(dict_a, dict_b))


class SetAttrsTest(TestCase):

    def test_setattrs_with_empty_attrs(self):
        class Dummy:
            pass

        obj = Dummy()
        setattrs(obj, [])
        self.assertFalse(hasattr(obj, 'foo'))

    def test_setattrs_with_multiple_attrs(self):
        class Dummy:
            pass

        obj = Dummy()
        attrs = [('foo', 1), ('bar', 2), ('baz', 3)]
        setattrs(obj, attrs)
        self.assertEqual(obj.foo, 1)
        self.assertEqual(obj.bar, 2)
        self.assertEqual(obj.baz, 3)

    def test_setattrs_overwrites_existing(self):
        class Dummy:
            foo = 0

        obj = Dummy()
        attrs = [('foo', 42)]
        setattrs(obj, attrs)
        self.assertEqual(obj.foo, 42)