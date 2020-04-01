import sys
import asyncio
import traceback

from .encode import encode
from .decode import decode


class Requetes:

    def __init__(self):
        self._requetes = {}

    # A utiliser comme décorateur pour créer des requêtes
    # @inst.add(200)
    def add(self, name=None, cmd=None):

        def _recup_func(function):

            name_ = _recup_func.name
            cmd_ = _recup_func.cmd

            if name_ is None:
                name_ = function.__name__

            # Requêtes spéciales sans cmd
            if name_ in ['_OTHER', '_EXCEPTION', '_ALL']:
                self._requetes[name_] = function
                return function

            if name_ not in self._requetes:
                self._requetes[name_] = {}

            self._requetes[name_][cmd_] = function

            return function

        # Pour une raison que je ne connais pas il ne trouve pas les
        #  variable name et cmd tout seul
        _recup_func.name = name
        _recup_func.cmd = cmd

        return _recup_func

    async def recv(self, msg, *args, **kwargs):

        requetes = decode(msg, ever_list=True)

        returns = []

        def return_(result):
            if isinstance(result, (list, tuple)):
                for r in result:
                    returns.append(r)

            elif result is not None:
                returns.append(result)

        for requete in requetes:

            nom = requete.get('N#')
            cmd = requete.get('C#')
            info = requete.get('I#', {})

            func = self._requetes.get(nom, {}).get(cmd)

            if func:
                # Appel de la fonction correspondant à la commande
                return_(await self.__call_fonc(func,
                                               requete, *args, **info, **kwargs))

            else:
                # Si la commande n'existe pas ou n'a pas été definie
                #   génére la fonction correspondant à OTHER

                func_autre = self._requetes.get('_OTHER')

                if func_autre:
                    return_(await self.__call_fonc(func_autre,
                                                   requete, cmd, nom, *args, **info, **kwargs))

            # Pour la fonction spécial appelée pour toute sorte de requête
            func_all = self._requetes.get('_ALL')

            if func_all:
                return_(await self.__call_fonc(func_all,
                                               requete, cmd, nom, *args, **info, **kwargs))

        return ''.join([encode(r) for r in returns]) if returns else None

    async def __call_fonc(self, fonction, requete, *args, **kwargs):

        async def call():
            if (asyncio.iscoroutine(fonction)
                    or asyncio.iscoroutinefunction(fonction)):
                return await fonction(requete, *args, **kwargs)
            else:
                return fonction(requete, *args, **kwargs)

        func_except = self._requetes.get('_EXCEPTION')

        if func_except:
            try:
                return await call()

            except Exception as e:
                exception = (e.__class__.__name__, str(e))
                suivis = traceback.format_exc()
                return await self.__call_fonc(func_except,
                                              requete, exception, suivis, *args, **kwargs)

        else:
            return await call()


# Raccourcis
class GET:
    cmdcode__ = 'GET'


class POST:
    cmdcode__ = 'POST'


class DELETE:
    cmdcode__ = 'DELETE'


class PUT:
    cmdcode__ = 'PUT'


class OPTIONS:
    cmdcode__ = 'OPTIONS'


class RESPONSE:

    def __getitem__(self, item):
        class Response:
            cmdcode__ = item

        return Response


RESPONSE = RESPONSE()
