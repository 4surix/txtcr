import unittest
import txtcr


class BasicTests(unittest.TestCase):

    def test_inherit_print_name(self):
        class TestClass(txtcr.param.S["{N#}"]):
            pomme = "rouge"

        test = txtcr.decode(txtcr.encode(TestClass))

        self.assertEqual("\"TestClass\"", str(test))

    def test_inherit_print_content(self):
        class TestClass(txtcr.param.S["{I#.pomme}"]):
            pomme = "rouge"
            nombre = 10
            fraise = ["rouge", "blanche"]

        test = txtcr.decode(txtcr.encode(TestClass))

        self.assertEqual("\"rouge\"", str(test))

    def test_inherit_print_full_class(self):
        class TestClass(txtcr.param.S["<{I#.pouf}>"]):
            test = 10

        test = txtcr.encode(TestClass)

        self.assertEqual('<N#"TestClass" S#"<{I#.pouf}>" I#{"test" 10}>', test)

    def test_inherit_print_fully_embedded_class(self):
        class ToBeInherited(txtcr.param.S["{N#}"]):
            pomme = "rouge"
            nombre = 10
            fraise = ["rouge", "blanche"]

        class TestClass(txtcr.param.S["<{I#.pouf}>"]):
            pouf = ToBeInherited
            patapouf = True

        test = txtcr.encode(TestClass)

        self.assertEqual('<N#"TestClass" S#"<{I#.pouf}>" I#{"pouf" <N#"ToBeInherited" S#"{N#}" '
                         'I#{"pomme" "rouge" "nombre" 10 "fraise" '
                         '["rouge" "blanche"]}> "patapouf" 1""}>',
                         test)

    def test_file(self):
        with txtcr.fichier('../exemples/fichier.tcr', 'w', indent=4) as tcr:
            tcr.pomme = "rouge"
            tcr.poire = "jaune"

        self.assertEqual("<:TCR: File Test>", str(tcr))


if __name__ == '__main__':
    unittest.main()
