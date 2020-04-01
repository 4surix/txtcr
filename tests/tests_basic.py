import unittest
import txtcr
import datetime


class BasicTests(unittest.TestCase):
    """
    The basic tests for the TCR module.
    More aimed tests can be found in other files, in order to add more coverage to the code
    """

    #
    # CLASSES INHERITANCE: GLOBAL COMPARISON
    #
    def test_inherit_strClass_print_full_class(self):
        class TestClass(txtcr.Param.S["<{I#.pouf}>"]):
            test = 10

        test = txtcr.encode(TestClass)
        self.assertEqual('<N#"TestClass" S#"<{I#.pouf}>" I#{"test" 10}>', test)

    def test_inherit_reprClass_print_full_class(self):
        class TestClass(txtcr.Param.R["<{I#.pouf}>"]):
            test = 10

        test = txtcr.encode(TestClass)
        self.assertEqual('<N#"TestClass" R#"<{I#.pouf}>" I#{"test" 10}>', test)

    def test_inheritance_dateClass_print_full_class(self):
        date = str(datetime.datetime.today())

        class TestClass(txtcr.Param.T[date]):
            test = 10

        test = txtcr.encode(TestClass)
        self.assertEqual('<N#"TestClass" T#"' + date + '" I#{"test" 10}>', test)

    #
    # CLASSES INHERITANCE: STR SPECIALS
    #
    def test_inherit_strClass_print_name(self):
        class TestClass(txtcr.Param.S["{N#}"]):
            pomme = "rouge"

        test = txtcr.decode(txtcr.encode(TestClass))

        self.assertEqual("TestClass", str(test))

    def test_inherit_strClass_print_content(self):
        class TestClass(txtcr.Param.S["{I#.pomme}"]):
            pomme = "rouge"
            nombre = 10
            fraise = ["rouge", "blanche"]

        test = txtcr.decode(txtcr.encode(TestClass))

        self.assertEqual("rouge", str(test))

    #
    # CLASSES INHERITANCE: REPR SPECIALS
    #
    def test_inherit_reprClass_print_name(self):
        class TestClass(txtcr.Param.R["{N#}"]):
            pomme = "rouge"

        test = txtcr.decode(txtcr.encode(TestClass))

        self.assertEqual("TestClass", repr(test))

    def test_inherit_reprClass_print_content(self):
        class TestClass(txtcr.Param.R["{I#.pomme}"]):
            pomme = "rouge"
            nombre = 10
            fraise = ["rouge", "blanche"]

        test = txtcr.decode(txtcr.encode(TestClass))

        self.assertEqual("rouge", repr(test))

    #
    # EMBEDDED CLASS WITH INHERITANCE
    #
    def test_inherit_print_fully_embedded_class(self):
        class ToBeInherited(txtcr.Param.S["{N#}"]):
            pomme = "rouge"
            nombre = 10
            fraise = ["rouge", "blanche"]

        class TestClass(txtcr.Param.S["<{I#.pouf}>"]):
            pouf = ToBeInherited
            patapouf = True

        test = txtcr.encode(TestClass)

        self.assertEqual('<N#"TestClass" S#"<{I#.pouf}>" I#{"pouf" <N#"ToBeInherited" S#"{N#}" '
                         'I#{"pomme" "rouge" "nombre" 10 "fraise" '
                         '["rouge" "blanche"]}> "patapouf" 1""}>',
                         test)

    #
    # FILE
    #
    def test_file(self):
        filepath = 'fichier.tcr'
        backuppath = 'tests/fichier.tcr'

        def test(path):
            # Concentrating on editing and "compiling"
            with txtcr.Fichier(path, 'w') as tcr:
                tcr["N#"] = "File Test"
                tcr.pomme = "rouge"
                tcr.poire = "jaune"

            self.assertEqual("<:TCR: File Test>", str(tcr), msg="File compiling in TCR")

            # Concentrating on what was saved in the file
            with txtcr.Fichier(path, 'w') as tcr2:
                tcr2["N#"] = "File Test"
                tcr2.pomme = "mangée"
                tcr2.poire = "pourrie"

            with open(path, 'r', encoding='utf-8') as f:
                c = f.read()

            self.assertEqual('<N#"File Test" I#{"pomme" "mangée" "poire" "pourrie"}>',
                             c,
                             msg="File: comparing saved TCR to expected")

        try:
            test(filepath)
        except FileNotFoundError:
            test(backuppath)


if __name__ == '__main__':
    unittest.main()
