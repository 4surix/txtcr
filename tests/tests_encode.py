
import unittest


import txtcr as tcr
import txtcr.core.types as types


class EncodingTests(unittest.TestCase):

    def test_str(self):
        test = "This is a string"
        self.assertEqual(f'"{test}"', tcr.encode(test))

    def test_bytes(self):
        test = b'test'
        self.assertEqual(f"'test'", tcr.encode(test))

    def test_bools(self):
        self.assertEqual('False', tcr.encode(False), msg="Builtin bool False")
        self.assertEqual('True', tcr.encode(True), msg="Builtin bool True")

    def test_nones(self):
        self.assertEqual('None', tcr.encode(None), msg="Builtin None")

    def test_int_float(self):
        self.assertEqual("4", tcr.encode(4), msg="Int")
        self.assertEqual("3.14", tcr.encode(3.14), msg="Float")

    def test_dict(self):
        test = {1: "test", 2: {"test": True}}
        self.assertEqual('{1 test 2 {test True}}', tcr.encode(test))

    def test_list(self):
        self.assertEqual('[0 1 2]', tcr.encode([0, 1, 2]))

    def test_tuple(self):
        self.assertEqual('(3 4 5)', tcr.encode((3, 4, 5)))


if __name__ == '__main__':
    unittest.main()
