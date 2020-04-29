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
        self.assertEqual('0""', tcr.encode(False), msg="Builtin bool False")
        self.assertEqual('1""', tcr.encode(True), msg="Builtin bool True")

        bool_false = types.TCRBool(False, "ceci est un test")
        bool_true = types.TCRBool(True, "un autre test")

        self.assertEqual('0"ceci est un test"', tcr.encode(bool_false), msg="TCR bool False")
        self.assertEqual('1"un autre test"', tcr.encode(bool_true), msg="TCR bool True")

    def test_nones(self):
        self.assertEqual('O""', tcr.encode(None), msg="Builtin None")

        none_commented = types.TCRNone("petit test")

        self.assertEqual('O"petit test"', tcr.encode(none_commented), msg="TCR none")

    def test_int_float(self):
        self.assertEqual("4", tcr.encode(4), msg="Int")
        self.assertEqual("3.14", tcr.encode(3.14), msg="Float")

    def test_dict(self):
        test = {1: "test", 2: {"test": True}}
        self.assertEqual('{1 "test" 2 {"test" 1""}}', tcr.encode(test))

    def test_list(self):
        self.assertEqual('[0 1 2]', tcr.encode([0, 1, 2]))

    def test_tuple(self):
        self.assertEqual('(3 4 5)', tcr.encode((3, 4, 5)))


if __name__ == '__main__':
    unittest.main()
