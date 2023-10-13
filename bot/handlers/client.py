import asyncio
import aiogram
from service import gameCodes
from service.player import Player
from service.game import Game
from aiogram import types, filters
from aiogram import Router
from bot import dp, bot, stack
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import ME

import texts

router = Router()

@router.message(F.chat.type.in_({"private"}),filters.Command('start'))
async def startCommand(message: types.Message, state: FSMContext):
    if ' ' in message.text and 'connect_' in message.text:
        index = int(message.text.replace('/start ', '').replace('start ', '').replace('connect_', ''))
        game = stack.getGame(index)
        if game.findPlayer(message.from_user.id):
                await message.answer(texts.client.U_IN_GAME)
                # return None
        player = Player(message.from_user.id, bot, index, message.from_user.full_name, username=message.from_user.username)
        game.addPlayer(player)
        inkb = InlineKeyboardBuilder()
        inkb.row(types.InlineKeyboardButton(text=texts.client.CONNECT_TO_GAME, url=f't.me/{ME}?start=connect_{str(index)}'))
        await game.messages['createMessage'].edit_text(texts.client.CONNECTED_MANS.format(countMans=len(game.players),players=game.getLinksPlayers()), parse_mode='markdown')
        # await asyncio.sleep(0.3)
        message.edit_reply_markup()
        await bot.edit_message_reply_markup(chat_id=index,message_id=game.messages['createMessage'].message_id,reply_markup=inkb.as_markup())
        await message.answer('Ты успешно присоединился к игре #{0}'.format(str(index).replace('-','')))

@router.message(F.chat.type.in_({"group", "supergroup"}), filters.Command('extend'))
async def connect_handler(message: types.Message, state: FSMContext):
    stack.getGame(message.chat.id).connectTime+=30
    await message.answer("Добавил вам 30 секунд")


@router.message(F.chat.type.in_({"group", "supergroup"}),filters.Command('create'))
async def createCommand(message: types.Message, state: FSMContext):
    index = message.chat.id
    game = Game(index, bot=bot, voteTime=30, connectTime = 120)
    try:
        await message.delete()
    except aiogram.utils.exceptions.MessageCantBeDeleted:
        await game.send_message('Я не могу удалять сообщения.')
    if not stack.addGame(game, index):
        return await game.send_message("Игра уже создана.")
    inkb = InlineKeyboardBuilder()
    inkb.row(types.InlineKeyboardButton(text=texts.client.CONNECT_TO_GAME, url=f't.me/{ME}?start=connect_{str(index)}'))
    message = await message.answer(texts.client.CONNECTED_MANS.format(countMans=0, players=''), reply_markup=inkb.as_markup())
    try:
        await message.pin()
    except:
        await message.reply("У меня нет прав, чтобы закрепить сообщение.")
    game.messages['createMessage'] = message
    response = await game.connectWaiter()
    if response == gameCodes.Codes.NOT_HAVE_PLAYERS:
        stack.removeGame(index)
        return await game.send_message(texts.client.NOT_HAVE_MORE_PLAYERS)

