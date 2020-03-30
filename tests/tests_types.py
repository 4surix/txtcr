import unittest
import txtcr.types as t


class TypesTests(unittest.TestCase):
    """
    This file is concentrating on tests to add coverage on the types.py file
    from the txtcr module.
    """

    #
    # bool class
    #
    def test_bool_class_init(self):
        b = t.bool(True, "this is a comment")

        self.assertEqual(True, b.value, msg="Value")
        self.assertEqual("this is a comment", b.commentaire, msg="Comment")

    def test_bool_class_bool_eq_ne(self):
        b = t.bool(True)

        self.assertEqual(True, bool(b), msg="__bool__")
        self.assertEqual(True, b == True, msg="__eq__")
        self.assertEqual(True, b != False, msg="__ne__")

    def test_bool_class_str_repr(self):
        b = t.bool(False, "false this time")

        self.assertEqual('False', repr(b), msg="__repr__")
        self.assertEqual('False #false this time', str(b), msg="__str__")

    def test_bool_class_index_hash(self):
        b = t.bool(True)
        c = t.bool(False)

        # Indexes
        self.assertEqual(1, b.__index__(), msg="TCRBool(True) index")
        self.assertEqual(0, c.__index__(), msg="TCRBool(False) index")

        # Hashes
        self.assertEqual(hash(True), hash(b), msg="TCRBool(True) hash")
        self.assertEqual(hash(False), hash(c), msg="TCRBool(False) hash")

    #
    # none class
    #
    def test_none_class_init(self):
        n = t.none("this is a comment")

        self.assertEqual("this is a comment", n.commentaire)

    def test_none_class_bool_eq_ne(self):
        n = t.none()

        self.assertEqual(False, bool(n), msg="__bool__")
        self.assertEqual(True, n == None, msg="__eq__")
        self.assertEqual(True, n != 2, msg="__ne__")

    def test_none_class_str_repr(self):
        n = t.none("another comment")

        self.assertEqual('None', repr(n), msg="__repr__")
        self.assertEqual('None #another comment', str(n), msg="__str__")

    def test_none_class_hash(self):
        n = t.none()

        self.assertEqual(hash(None), hash(n))


if __name__ == '__main__':
    unittest.main()
