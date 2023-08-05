# -*- coding: UTF-8 -*-
import unittest

from pandasticsearch.operators import *
from pandasticsearch.types import Row, Column


class TestSchema(unittest.TestCase):
    def test_row(self):
        row = Row(a=1, b='你好,世界')
        self.assertEqual(row['a'], 1)
        self.assertEqual(row['b'], '你好,世界')
        self.assertEqual(row.as_dict(), {'a': 1, 'b': '你好,世界'})

    def test_column(self):
        col_a = Column('a')
        col_b = Column('b')

        self._assert_equal_filter(col_b > 2, Greater('b', 2))
        self._assert_equal_filter(~(col_b > 2), ~Greater('b', 2))
        self._assert_equal_filter(col_b >= 2, GreaterEqual('b', 2))
        self._assert_equal_filter(col_b < 2, Less('b', 2))
        self._assert_equal_filter(col_b <= 2, LessEqual('b', 2))
        self._assert_equal_filter(col_b == 2, Equal('b', 2))
        self._assert_equal_filter(col_b != 2, ~Equal('b', 2))
        self._assert_equal_filter((col_a > 2) & (col_b < 1), Greater('a', 2) & Less('b', 1))
        self._assert_equal_filter(col_b.isin([1, 2, 3]), IsIn('b', [1, 2, 3]))
        self._assert_equal_filter(~col_b.isin([1, 2, 3]), ~IsIn('b', [1, 2, 3]))

        self._assert_equal_filter(col_b.like('a*b'), Like('b', 'a*b'))
        self._assert_equal_filter(col_b.rlike('a*b'), Rlike('b', 'a*b'))
        self._assert_equal_filter(col_b.startswith('jj'), Startswith('b', 'jj'))
        self._assert_equal_filter(col_b.isnull, IsNull('b'))
        self._assert_equal_filter(col_b.notnull, NotNull('b'))

    def _assert_equal_filter(self, x, y):
        self.assertTrue(x, BooleanFilter)
        self.assertTrue(y, BooleanFilter)
        self.assertEqual(x.build(), y.build())


if __name__ == '__main__':
    unittest.main()
