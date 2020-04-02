import txtcr
import websockets

from txtcr.requests.requete import *  # Requetes, POST, GET, ...


class INFO:
    phrase = None
    users = {}


### Création des requetes

reqserv = txtcr.requests.requete.Requetes()


# Création d'une requête CONNEXION
# qui répondra à la commande POST
@reqserv.add(name='CONNEXION', cmd='POST')
def add_client(requete, client, *, id:int):

    # Ajout du client
    INFO.users[id] = client

    class CONNEXION(RESPONSE[200]):
        status = 'Connectée.'

    # Renvoie la requete CONNEXION au client
    return CONNEXION


# Création d'une requête PHRASE
# qui répondra à la commande GET
@reqserv.add(name='PHRASE', cmd='GET')
def client_recup_phrase(requete, client):

    class PHRASE(RESPONSE[200]):
        phrase = INFO.phrase

    # Renvoie la requete PHRASE au client
    return PHRASE


@reqserv.add(name='PHRASE', cmd='POST')
async def modif_phrase(requete, client, *, phrase:str=None):

    print(INFO.phrase, '->', phrase)

    INFO.phrase = phrase

    class PHRASE(RESPONSE[200]):
        phrase = INFO.phrase

    reponse = txtcr.encode(PHRASE)

    for user in INFO.users.values():
        await user.send(reponse)


@reqserv.add('_EXCEPTION')
def _EXCEPTION(requete, client, *args, **kwargs):

    print(args, kwargs)

    # Ne retourne rien


### Serveur

async def reception_client(websocket, path):
    
    try:
        while True:
            reçu = await websocket.recv()
            reponse = await reqserv.recv(reçu, websocket)
            if reponse:
                await websocket.send(reponse)

    except websockets.exceptions.ConnectionClosed:
        # Si un client se déconecte du serveur
        for cid, client in INFO.users.items():
            if client == websocket:
                del INFO.users[cid]
                break


async def run():
    print('Serveur prêt.')

    await websockets.serve(reception_client, '127.0.0.1', 6000)

# ---------------

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
loop.run_forever()

# ----------------