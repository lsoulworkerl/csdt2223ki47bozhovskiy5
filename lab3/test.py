from unittest import TestCase, main
from lab2 import parser


class CalculatorTest(TestCase):
    def test_output(self):
        self.assertEqual(parser(1), 2)

    def test_output1(self):
        self.assertEqual(parser(2), 4)

    def test_output2(self):
        self.assertEqual(parser(3), 6)


if __name__=='__main__':
    main()
