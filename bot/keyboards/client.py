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

def getInkbOpenStats(game, opened, selected):
    inkb = InlineKeyboardBuilder()
    if not opened['sex']:
        if selected == 'sex':
            inkb.button(text='Пол ✅', callback_data=Select(action='sex', game=game))
        else:
            inkb.button(text='Пол', callback_data=Select(action='sex', game=game))
    if not opened['age']:
        if selected == 'age':
            inkb.button(text='Возраст ✅', callback_data=Select(action='age', game=game))
        else:
            inkb.button(text='Возраст', callback_data=Select(action='age', game=game))
    if not opened['body']:
        if selected == 'body':
            inkb.button(text='Телосложение ✅', callback_data=Select(action='body', game=game))
        else:
            inkb.button(text='Телосложение', callback_data=Select(action='body', game=game))
    if not opened['heal']:
        if selected == 'heal':
            inkb.button(text='Здоровье ✅', callback_data=Select(action='heal', game=game))
        else:
            inkb.button(text='Здоровье', callback_data=Select(action='heal', game=game))
    if not opened['phobia']:
        if selected == 'phobia':
            inkb.button(text='Фобия ✅', callback_data=Select(action='phobia', game=game))
        else:
            inkb.button(text='Фобия', callback_data=Select(action='phobia', game=game))
    if not opened['hobby']:
        if selected == 'hobby':
            inkb.button(text='Хобби ✅', callback_data=Select(action='hobby', game=game))
        else:
            inkb.button(text='Хобби', callback_data=Select(action='hobby', game=game))
    if not opened['utils']:
        if selected == 'utils':
            inkb.button(text='Дополнительный факт ✅', callback_data=Select(action='utils', game=game))
        else:
            inkb.button(text='Дополнительный факт', callback_data=Select(action='utils', game=game))
    inkb.adjust(1,1,1,1,1,1,1,1)
    return inkb.as_markup()


def getInkOfVote(game:int,players):
    players_adjust = [1 for i in range(0,len(players))]
    inkb = InlineKeyboardBuilder()
    for player in players:
        if player.live:
            inkb.button(text=f'{player.full_name}| {player.getVoted()}',
                    callback_data=VotePlayerCallbackData(game=game, playerId=player.id))
    inkb.adjust(*players_adjust)
    return inkb.as_markup()


def getInkbOpenedStats(game, players_list:list):
    players_adjust = [1 for i in range(0,len(players_list))]
    inkb = InlineKeyboardBuilder()
    players_list = [player[0] for player in players_list]
    for player in players_list:
        if player.live:
            inkb.button(text=f'Показать {player.full_name}', callback_data=OpenedCallbackData(game=game, playerId=player.id))
    inkb.adjust(*players_adjust)
    return inkb.as_markup()