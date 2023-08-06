"""
@brief      test log(time=3s)
"""

import sys
import os
import unittest
from pyquickhelper.pycode import ExtTestCase


try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src


from src.wrapclib import re2


class TestMatch(ExtTestCase):

    def test_const_match(self):
        m = re2.match('abc', 'abc')
        self.assertIsNotNone(m)
        self.assertEqual(m.start(), 0)
        self.assertEqual(m.end(), 3)
        self.assertEqual(m.span(), (0, 3))
        self.assertEqual(m.groups(), tuple())
        self.assertEqual(m.groupdict(), {})
        self.assertEqual(m.pos, 0)
        self.assertEqual(m.endpos, 3)
        self.assertEqual(m.string, 'abc')
        self.assertIsNotNone(m.re)
        self.assertEqual(m.re.pattern, 'abc')
        self.assertEqual(m.re.groups, 0)
        self.assertEqual(m.re.groupindex, {})

    def test_group_match(self):
        m = re2.match('ab([cde]fg)', 'abdfghij')
        self.assertIsNotNone(m)
        self.assertEqual(m.start(), 0)
        self.assertEqual(m.end(), 5)
        self.assertEqual(m.span(), (0, 5))
        self.assertEqual(m.groups(), ('dfg',))
        self.assertEqual(m.groupdict(), {})
        self.assertEqual(m.pos, 0)
        self.assertEqual(m.endpos, 8)
        self.assertEqual(m.string, 'abdfghij')
        self.assertIsNotNone(m.re)
        self.assertEqual(m.re.pattern, 'ab([cde]fg)')
        self.assertEqual(m.re.groups, 1)
        self.assertEqual(m.re.groupindex, {})

    def test_named_group_match(self):
        m = re2.match('ab(?P<testgroup>[cde]fg)', 'abdfghij')
        self.assertIsNotNone(m)
        self.assertEqual(m.start(), 0)
        self.assertEqual(m.end(), 5)
        self.assertEqual(m.span(), (0, 5))
        self.assertEqual(m.groups(), ('dfg',))
        self.assertEqual(m.groupdict(), {'testgroup': 'dfg'})
        self.assertEqual(m.pos, 0)
        self.assertEqual(m.endpos, 8)
        self.assertEqual(m.string, 'abdfghij')
        self.assertIsNotNone(m.re)
        self.assertEqual(m.re.pattern, 'ab(?P<testgroup>[cde]fg)')
        self.assertEqual(m.re.groups, 1)
        self.assertEqual(m.re.groupindex, {'testgroup': 1})

    def test_compiled_match(self):
        r = re2.compile('ab([cde]fg)')
        m = r.match('abdfghij')
        self.assertIsNotNone(m)
        self.assertEqual(m.start(), 0)
        self.assertEqual(m.end(), 5)
        self.assertEqual(m.span(), (0, 5))
        self.assertEqual(m.groups(), ('dfg',))
        self.assertEqual(m.groupdict(), {})
        self.assertEqual(m.pos, 0)
        self.assertEqual(m.endpos, 8)
        self.assertEqual(m.string, 'abdfghij')
        self.assertIsNotNone(m.re)
        self.assertEqual(m.re.pattern, 'ab([cde]fg)')
        self.assertEqual(m.re.groups, 1)
        self.assertEqual(m.re.groupindex, {})

    def test_match_raise(self):
        '''test that using the API incorrectly fails'''
        r = re2.compile('ab([cde]fg)')
        self.assertRaise(lambda: re2.match(r, 'abdfghij'), TypeError)

    def test_match_bytes(self):
        ''' test that we can match things in the bytes type '''
        r = re2.compile('(\\x09)')
        m = r.match(b'\x09')
        self.assertIsNotNone(m)
        g = m.groups()
        self.assertTrue(isinstance(g, tuple))
        self.assertTrue(isinstance(g[0], bytes))
        self.assertEqual(b'\x09', g[0])
        self.assertEqual(m.pos, 0)
        self.assertEqual(m.endpos, 1)
        self.assertEqual(m.string, b'\x09')
        self.assertIsNotNone(m.re)
        self.assertEqual(m.re.pattern, '(\\x09)')
        self.assertEqual(m.re.groups, 1)
        self.assertEqual(m.re.groupindex, {})

    def test_match_str(self):
        ''' test that we can match binary things in the str type '''
        r = re2.compile('(\\x09)')
        m = r.match('\x09')
        self.assertIsNotNone(m)
        g = m.groups()
        self.assertTrue(isinstance(g, tuple))
        self.assertTrue(isinstance(g[0], str))
        self.assertEqual('\x09', g[0])

    def test_match_bad_utf8_bytes(self):
        ''' Validate that we just return None on invalid utf-8 '''
        r = re2.compile('\\x80')
        m = r.match(b'\x80')
        self.assertIsNone(m)

    def test_invalid_pattern(self):
        ''' Verify that bad patterns raise an exception '''
        self.assertRaise(lambda: re2.compile(')'), Exception)

    def test_span_type(self):
        ''' verify that start/end return the native literal integer type '''
        r = re2.compile('abc')
        m = r.match('abc')
        self.assertTrue(isinstance(m.start(), type(1)))
        self.assertTrue(isinstance(m.end(), type(1)))

    def test_set_unanchored(self):
        s = re2.Set(re2.UNANCHORED)
        s_with_default_anchoring = re2.Set()

        for re2_set in [s, s_with_default_anchoring]:
            re2_set.add('foo')
            re2_set.add('bar')
            re2_set.add('baz')
            re2_set.compile()

            self.assertEqual(re2_set.match('foo'), [0])
            self.assertEqual(re2_set.match('bar'), [1])
            self.assertEqual(re2_set.match('baz'), [2])
            self.assertEqual(re2_set.match('afoobaryo'), [0, 1])

            self.assertEqual(re2_set.match('ooba'), [])

    def test_set_anchor_both(self):
        s = re2.Set(re2.ANCHOR_BOTH)
        self.assertEqual(s.add('foo'), 0)
        self.assertEqual(s.add('bar'), 1)
        s.compile()

        self.assertEqual(s.match('foobar'), [])
        self.assertEqual(s.match('fooba'), [])
        self.assertEqual(s.match('oobar'), [])
        self.assertEqual(s.match('foo'), [0])
        self.assertEqual(s.match('bar'), [1])

    def test_set_anchor_start(self):
        s = re2.Set(re2.ANCHOR_START)
        self.assertEqual(s.add('foo'), 0)
        self.assertEqual(s.add('bar'), 1)
        s.compile()

        self.assertEqual(s.match('foobar'), [0])
        self.assertEqual(s.match('oobar'), [])
        self.assertEqual(s.match('foo'), [0])
        self.assertEqual(s.match('ofoobaro'), [])
        self.assertEqual(s.match('baro'), [1])

    def test_bad_anchoring(self):
        self.assertRaise(lambda: re2.Set(None), ValueError,
                         'anchoring must be one of')
        self.assertRaise(lambda: re2.Set(15), ValueError,
                         'anchoring must be one of')
        self.assertRaise(lambda: re2.Set({}), ValueError,
                         'anchoring must be one of')

    def test_match_without_compile(self):
        s = re2.Set()
        s.add('foo')
        self.assertRaise(lambda: s.match('bar'),
                         RuntimeError, 'Can\'t match() on an')

    def test_add_after_compile(self):
        s = re2.Set()
        s.add('foo')
        s.compile()
        self.assertRaise(lambda: s.add('bar'), RuntimeError,
                         'Can\'t add() on an already compiled Set')

    def test_double_compile(self):
        s = re2.Set()
        s.add('foo')
        s.compile()
        s.compile()

    def test_add_with_bad_pattern(self):
        s = re2.Set()
        self.assertRaise(lambda: s.add('('), ValueError, 'missing')
        self.assertRaise(lambda: s.add(3), TypeError)

    def test_findall(self):
        s = """date 0 : 14/9/2000 date 1 : 20/04/1971 """
        reg = re2.compile(
            "([0-3]?[0-9]/[0-1]?[0-9]/([0-2][0-9])?[0-9][0-9])[^\\d]")
        res = reg.search(s, 0)
        self.assertEqual(res.groups(), ('14/9/2000', '20'))
        self.assertEqual(res.pos, 0)
        self.assertEqual(res.endpos, 39)
        self.assertEqual(res.span(), (9, 19))
        fall = re2.findall(reg, s)
        self.assertEqual(fall, [('14/9/2000', '20'), ('20/04/1971', '19')])
        fall = re2.findall(
            "([0-3]?[0-9]/[0-1]?[0-9]/([0-2][0-9])?[0-9][0-9])[^\\d]", s)
        self.assertEqual(fall, [('14/9/2000', '20'), ('20/04/1971', '19')])


if __name__ == "__main__":
    unittest.main()
