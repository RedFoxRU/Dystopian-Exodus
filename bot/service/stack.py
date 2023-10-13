import typing
from service.game import Game


class Stack ():
    
    def __init__(self):
        self.games = {}
        self.searchers = []

    def getGame(self, id) -> typing.Union[Game, None]:
        if f"{id}" in self.games.keys():
            return self.games[f'{id}']
        else:
            return None

    def addGame(self, game:Game, id: typing.Union[int,typing.Text]) -> bool:
        if self.getGame(id):
            return False
        else:
            self.games[f'{id}'] = game
            return True

    def removeGame(self, game) -> bool:
        if str(game) in self.games.keys():
            del self.games[f'{game}']
            return True
        else:
            return False

