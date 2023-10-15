from aiogram import Router, types
from bot import stack
from keyboards.client import (Select, VotePlayerCallbackData,
                            OpenedCallbackData)
from service.player import Player

router = Router()

@router.callback_query(Select.filter())
async def callbacks_num_change_fab(
                callback: types.CallbackQuery, 
                callback_data: Select):
    stack.getGame(id=callback_data.game).getPlayer(callback.from_user.id).select_to_open(callback_data.action)
    await stack.getGame(id=callback_data.game).getPlayer(callback.from_user.id).edit_opened_stats()

@router.callback_query(VotePlayerCallbackData.filter())
async def callback_vote_to(
    callback: types.CallbackQuery,
    callback_data: VotePlayerCallbackData):
    game = stack.getGame(id=callback_data.game)
    if not game.checkPlayer(callback.from_user.id):
        return
    if game.getPlayer(callback_data.playerId) != game.getPlayer(callback.from_user.id).votedIn:
        try:
            game.getPlayer(callback_data.votedIn).voted -=1
        except: 
            pass
        game.getPlayer(callback.from_user.id).voteIn(game.getPlayer(callback_data.playerId))
        await game.updateVoteReply()
    

@router.callback_query(OpenedCallbackData.filter())
async def callback_open_stats(
    callback: types.CallbackQuery,
    callback_data: OpenedCallbackData):
    game = stack.getGame(id=callback_data.game)
    player:Player = game.getPlayer(callback_data.playerId)
    await player.send_opened_stats_to(callback.from_user.id)