"""
Exemple de client utilisant websocket et txtcr.
Ouvrez plusieurs client pour tester !
"""

import txtcr

import random
import asyncio
import websockets

from txtcr.requete import *  # Requetes, POST, GET, ...
from aioconsole import ainput


### Mise en place des requêtes

reqclt = txtcr.requete.Requetes()


@reqclt.add(cmd=200)
def CONNEXION(requete, status):

    print('STATUS:', status)

    # Ne renvoie rien au serveur


@reqclt.add(cmd=200)
def PHRASE(requete, phrase):
    
    print('PHRASE:', phrase)

    # Ne renvoie rien au serveur


### Mise en place du client

class Client:

    def __init__(self):

        self.url = "ws://127.0.0.1:6000"

        self.ws = True

    async def start(self):

        class CONNEXION(POST):
            id = random.randint(0, 100000)

        class TEST(POST):
            pass
        réponse = txtcr.encode(CONNEXION) + txtcr.encode(TEST)

        while True:

            if réponse:
                await self.ws.send(réponse)

            réponse = await reqclt.recv(await self.ws.recv())

    async def run(self):

        self.ws = await websockets.connect(self.url)

        try:
            await self.start()

        except websockets.exceptions.ConnectionClosed:
            # Si le serveur se déconnecte
            self.ws = None

client = Client()


async def run_prog():

    print("Ecrivez n'importe quel texte, cela l'envera au serveur."
        + "\nEcrivez 'GET' pour récupérer le dernier texte envoyé.")

    while client.ws:

        texte = await ainput()

        if not client.ws:
            break

        if texte == 'GET':

            class PHRASE(GET):
                pass

        else:

            class PHRASE(POST):
                phrase = texte

        await client.ws.send(txtcr.encode(PHRASE))


# -----------------------

loop = asyncio.get_event_loop()
asyncio.ensure_future(client.run())
asyncio.ensure_future(run_prog())
loop.run_forever()

# -------------------