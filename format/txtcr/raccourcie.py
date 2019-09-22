
# Param ---------------------
class param:

    class R:

        def __getitem__(ss, item):
            class R:
                __irepr__ = item
            return R
        
    R = R()

    class S:

        def __getitem__(ss, item):
            class S:
                __istr__ = item
            return S
        
    S = S()

    class T:

        def __getitem__(ss, item):
            class T:
                __date__ = item
            return T
        
    T = T()

# Requêtes ------------------
class GET:
    __cmdcode__ = 'GET'

class POST:
    __cmdcode__ = 'POST'

class DELETE:
    __cmdcode__ = 'DELETE'

class OPTIONS:
    __cmdcode__ = 'OPTIONS'

class RESPONSE:

    def __getitem__(ss, item):
        class RESPONSE:
            __cmdcode__ = item
        return RESPONSE
    
RESPONSE = RESPONSE()