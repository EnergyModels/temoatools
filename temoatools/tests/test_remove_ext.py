import unittest
import temoatools as tt


class TestRemoveExt(unittest.TestCase):

    def test_remove_ext(self):

        filename = "longFileName1234.sqlite"
        result = tt.remove_ext(filename)
        expected = "longFileName1234"
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()