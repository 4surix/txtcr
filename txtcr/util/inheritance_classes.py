class Param:
    """
    Allows to create a class than inherits the given TCR parameter
    Permet de créer une classe qui va hériter d'un paramètre TCR.

    Params:
    - S / STR => class reaction to str() call
    - R / REPR => class reaction to repr() call
    - T / DATE => date the TCR was created at, or anything relevant. This parameter is always user-stated.

    Exemple:
        class Test(txtcr.Param.REPR["<{I#.pouf}>"]):
            # cette classe va hériter de la capacité à afficher la valeur de pouf (rouge) lors d'un repr() de la classe
            # this class will inherit capacity to print pouf value (rouge) when you call repr() with this class or inst
            pouf = rouge
    """

    class PrebuiltRepr:

        def __getitem__(self, item):
            class R:
                repr__ = item

            return R

    R = REPR = PrebuiltRepr()

    class PrebuiltStr:

        def __getitem__(self, item):
            class S:
                str__ = item

            return S

    S = STR = PrebuiltStr()

    class PrebuiltTime:

        def __getitem__(self, item):
            class T:
                date__ = item

            return T

    T = DATE = PrebuiltTime()

