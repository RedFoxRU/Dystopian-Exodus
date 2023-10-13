from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData



class Select(CallbackData, prefix="open"):
    action: str
    game: int

class VotePlayerCallbackData(CallbackData, prefix='vote'):
    game: int
    playerId: int

class OpenedCallbackData(CallbackData, prefix='opened'):
    game: int
    playerId: int

def getInkbOpenStats(game):
    inkb = InlineKeyboardBuilder()
    inkb.button(text='Пол', callback_data=Select(action='sex', game=game))
    inkb.button(text='Возраст', callback_data=Select(action='age', game=game))
    inkb.button(text='Телосложение', callback_data=Select(action='body', game=game))
    inkb.button(text='Здоровье', callback_data=Select(action='heal', game=game))
    inkb.button(text='Фобия', callback_data=Select(action='phobia', game=game))
    inkb.button(text='Хобби', callback_data=Select(action='hobby', game=game))
    inkb.button(text='Разное', callback_data=Select(action='utils', game=game))
    inkb.adjust(1,1,1,1,1,1,1,1)
    return inkb.as_markup()


def getInkOfVote(game:int,players):
    players_adjust = [1 for i in range(0,len(players))]
    inkb = InlineKeyboardBuilder()
    for player in players:
        inkb.button(text=f'{player.full_name}| {player.getVoted()}',
                    callback_data=VotePlayerCallbackData(game=game, playerId=player.id))
    inkb.adjust(*players_adjust)
    return inkb.as_markup()


def getInkbOpenedStats(game, players_list:list):
    players_adjust = [1 for i in range(0,len(players_list))]
    inkb = InlineKeyboardBuilder()
    players_list = [player[0] for player in players_list]
    for player in players_list:
        inkb.button(text=f'Показать {player.full_name}', callback_data=OpenedCallbackData(game=game, playerId=player.id))
    inkb.adjust(*players_adjust)
    return inkb.as_markup()