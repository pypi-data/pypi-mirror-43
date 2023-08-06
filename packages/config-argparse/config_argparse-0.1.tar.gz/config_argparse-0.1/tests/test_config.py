import unittest
import argparse
from config_argparse import Config, DynamicConfig


class TestConfig(unittest.TestCase):

    def test_parse_args(self):

        class C(Config):
            a = 1

        c = C()
        cc = c.parse_args([])
        self.assertEqual(cc.a, 1, 'default value')
        cc = c.parse_args(['--a', '10'], namespace=cc)
        self.assertEqual(cc.a, 10, 'update works')
        cc = c.parse_args(['--a', '100'], namespace=cc)
        self.assertEqual(cc.a, 100, 'update multiple times works')

    def test_parse_basic_types(self):

        class C(Config):
            str = 'test'
            int = 1
            float = 1.0
            bool = False

        c = C()
        cc = c.parse_args([
            '--str',
            'foo',
            '--int',
            '10',
            '--float',
            '10.5',
            '--bool',
        ])
        self.assertEqual(cc.str, 'foo', 'str')
        self.assertEqual(cc.int, 10, 'int')
        self.assertEqual(cc.float, 10.5, 'float')
        self.assertEqual(cc.bool, True, 'bool')

    def test_list(self):

        class C(Config):
            a = [1, 2, 3]

        c = C()
        cc = c.parse_args([])
        self.assertEqual(cc.a, [1, 2, 3], 'default value')
        cc = c.parse_args(['--a', '1', '3', '5'], namespace=cc)
        self.assertEqual(cc.a, [1, 3, 5], 'update works')

    def test_parse_nested(self):

        class Nest(Config):
            a = 1

        class C(Config):
            a = 0.1
            nest = Nest()

        c = C()
        cc = c.parse_args([])
        self.assertEqual(cc.a, 0.1, 'default value')
        self.assertEqual(cc.nest.a, 1, 'default value in nest')
        cc = c.parse_args(['--nest.a', '10'], namespace=cc)
        self.assertEqual(cc.a, 0.1, 'should not be overwritten')
        self.assertEqual(cc.nest.a, 10, 'should be overwritten')

    def test_parse_nested_nested(self):

        class NestNest(Config):
            a = 'str'

        class Nest(Config):
            a = 1
            nest = NestNest()

        class C(Config):
            a = 0.1
            nest = Nest()

        c = C()
        cc = c.parse_args([])
        self.assertEqual(cc.a, 0.1, 'default value')
        self.assertEqual(cc.nest.a, 1, 'default value in nest')
        self.assertEqual(
            cc.nest.nest.a, 'str', 'default value in nest in nest'
        )

        cc = c.parse_args(['--nest.nest.a', '10'], namespace=cc)
        self.assertEqual(cc.a, 0.1, 'should not be overwritten')
        self.assertEqual(cc.nest.a, 1, 'should not be overwritten')
        self.assertEqual(cc.nest.nest.a, '10', 'should be overwritten')

    def test_parse_dynamic(self):

        class NestA(Config):
            a = 'str'

        class NestB(Config):
            b = 1

        class C(Config):
            a = 0.1
            nest = 'a'
            nest_cfg = DynamicConfig(
                lambda c: NestA() if c.nest == 'a' else NestB()
            )

        c = C()
        cc = c.parse_args([])

        self.assertTrue(
            isinstance(cc.nest_cfg, NestA),
            'nest_cfg should be NestA, but {}'.format(type(cc.nest_cfg))
        )
        self.assertEqual(cc.nest_cfg.a, 'str')

        cc = c.parse_args(['--nest', 'b'])
        self.assertTrue(
            isinstance(cc.nest_cfg, NestB),
            'nest_cfg should be NestB, but {}'.format(type(cc.nest_cfg))
        )
        self.assertFalse(hasattr(cc.nest_cfg, 'a'))
        self.assertEqual(cc.nest_cfg.b, 1)

        cc = c.parse_args(['--nest', 'b', '--nest_cfg.b', '100'])
        self.assertTrue(isinstance(cc.nest_cfg, NestB))

        self.assertEqual(cc.nest_cfg.b, 100)

    def test_inherit(self):

        class CC1(Config):
            a = 0.1

        class CC2(Config):
            b = 'str'

        class C(CC1, CC2):
            c = 1

        c = C()
        cc = c.parse_args([])
        self.assertEqual(cc.a, 0.1)
        self.assertEqual(cc.b, 'str')
        self.assertEqual(cc.c, 1)

        cc = c.parse_args(['--a', '0.2', '--b', 'foo', '--c', '2'])
        self.assertEqual(cc.a, 0.2)
        self.assertEqual(cc.b, 'foo')
        self.assertEqual(cc.c, 2)

    def test_inherit_overwrite(self):

        class CC1(Config):
            a = 0.1

        class C(CC1):
            a = 'str'

        c = C()
        cc = c.parse_args([])
        self.assertEqual(cc.a, 'str')

        cc = c.parse_args(['--a', 'foo'])
        self.assertEqual(cc.a, 'foo')


if __name__ == "__main__":
    unittest.main()