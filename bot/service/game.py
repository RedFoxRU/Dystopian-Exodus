import random
from asyncio import sleep
import typing

from aiogram import Bot, types
import aiogram
from service import gameCodes
from service.gameCodes import Codes

from service.player import Player
import texts
from texts import characters
from keyboards.client import getInkOfVote, getInkbOpenedStats

class Game():

    def __init__(self, chat, bot: Bot, voteTime:int, connectTime: int = 40,voiceMode: bool = False):
        self.id = chat
        self.bot = bot
        self.players = []
        self.messages = {
            'connectTimes': [],
        }
        self.connect = True
        self.connectTime = connectTime
        self.voiceMode = voiceMode
        self.voteTime = voteTime

    async def send_message(self, text: typing.Text,
                        parse_mode: typing.Optional[typing.Text] = 'Markdown',
                        entities: typing.Optional[typing.List[types.MessageEntity]] = None,
                        disable_web_page_preview: typing.Optional[bool] = None,
                        message_thread_id: typing.Optional[int] = None,
                        disable_notification: typing.Optional[bool] = None,
                        protect_content: typing.Optional[bool] = None,
                        reply_to_message_id: typing.Optional[int] = None,
                        allow_sending_without_reply: typing.Optional[bool] = None,
                        reply_markup: typing.Union[types.InlineKeyboardMarkup,
                                                    types.ReplyKeyboardMarkup,
                                                    types.ReplyKeyboardRemove,
                                                    types.ForceReply, None] = None,
                        ) -> types.Message:
        return await self.bot.send_message(self.id, text=text, parse_mode=parse_mode, entities=entities,
                                            disable_web_page_preview=disable_web_page_preview,
                                            message_thread_id=message_thread_id,
                                            disable_notification=disable_notification,
                                            protect_content=protect_content,
                                            reply_to_message_id=reply_to_message_id,
                                            allow_sending_without_reply=allow_sending_without_reply, reply_markup=reply_markup)

    
    def getPlayer(self, id:int)->Player:
        for player in self.players:
            if player.id == id:
                return player
        return None

    def checkPlayer(self, id):
        player: Player = self.getPlayer(id)
        if not player or player.live:
            return False
        return True


    
    def getAlivePlayersCount(self):
        alives_count = 0
        player: Player
        for player in self.players:
            if player.live:
                alives_count += 1
        return alives_count

    def gameOverCheck(self) -> Codes:
        if self.getAlivePlayersCount() == self.sleepCount:
            return Codes.GAME_OVER
        else:
            return None

    async def updateVoteReply(self):
        message: types.Message = self.messages['voteMessage']
        try:
            await self.bot.edit_message_reply_markup(chat_id=self.id, message_id=message.message_id,reply_markup=getInkOfVote(game=self.id, players=self.players))
        except:
            pass
        
        
    async def startVote(self):
        self.messages['voteMessage'] = await self.send_message(text=texts.client.START_VOTE, reply_markup=getInkOfVote(game=self.id, players=self.players))
        i = 0
        while i<30:
            voted_count = 0
            player: Player
            for player in self.players:
                if player.votedIn !=  0:
                    voted_count += 1
            if voted_count == self.getAlivePlayersCount():
                await self.messages['voteMessage'].delete()
                return
            await sleep(1)
            i+=1

        await self.messages['voteMessage'].delete()
        return
    
    def getMaxVoted(self):
        mvoted: Player = self.players[0]
        player: Player
        for player in self.players[1:]:
            if mvoted.voted < player.voted:
                mvoted = player
        return mvoted
    
    def getLinksPlayers(self) -> typing.Text:
        if len(self.players)>0:
            a = ''
            for player in self.players:
                a+= f'{player.link}\n'
            return a
        else:
            return ''

    def genBunker(self):
        if len(self.players) <= 4:
            n = 3
            s = 3
        elif len(self.players) <= 6: 
            n = 4
            s = 4
        else:
            n= 4
            s= 5
        self.food = random.randint(0, n)
        self.water = random.randint(0, n)
        self.sleepCount = random.randint(2, s)
        self.alivePlayers = len(self.players)


    def addPlayer(self, player: Player) -> bool:
        if len(self.players) >= 15:
            return gameCodes.MAX_PLAYERS
        if player not in self.players:
            self.players.append(player)
            return True
        else:
            return False
    
    def findPlayer(self, id:int) -> Player:
        if len(self.players) == 0:
            return None
        for player in self.players:
            if player.id == id:
                return player

    async def sendOpen(self, player_opened) -> None:
        players_links1, players_links2 = player_opened[:10], player_opened[10:]
        links1 = ''
        links2 = ''
        for link in players_links1:
            if link[0].live:
                links1 += link[1]+'\n'+'\n'
        for link in players_links2:
            if link[0].live:
                links2 += link[1]+'\n'+'\n'
        await self.send_message(links1, reply_markup=getInkbOpenedStats(game=self.id, players_list=players_links1))
        try:
            await self.send_message(links2, reply_markup=getInkbOpenedStats(game=self.id, players_list=players_links2))
        except aiogram.exceptions.TelegramBadRequest:
            pass

    def getPlayers(self) -> typing.List[Player]:
        return self.players

    def set_players_job(self) -> None:
        self.jobs = characters.jobs.copy()
        for player in self.players:
            job = player.set_job(jobs=self.jobs)
            self.jobs.remove(job)
    
    async def delete_keyboard(self):
        player: Player
        for player in self.players:
            if self._round == 1:
                await self.bot.edit_message_reply_markup(chat_id=player.openMessage.chat.id,
                                                        message_id=player.openMessage.message_id,
                                                        reply_markup=None)
            else:
                try:
                    await player.openMessage.delete()
                except:
                    pass
    
    async def mainloop(self):
        self.set_players_job()
        self._round = 1
        while True:
            for player in self.players:
                await player.send_stats()
            await self.send_message(texts.client.BUNKER_STATS.format(
                water=self.water,
                food=self.food,
                sleeper=self.sleepCount,
                _round=self._round )
                )
            await sleep(50)
            await self.delete_keyboard()
            players_links = []
            player: Player
            for player in self.players:
                opened = await player.open()
                players_links.append([player, f"{player.link} открыл {opened}"])
            await self.sendOpen(players_links)
            await self.send_message("Даю вам полторы минуты все обсудить")
            await sleep(90)
            
            if self._round > 1:
                await self.startVote()
                mvoted = self.getMaxVoted()
                if mvoted.voted != 0:
                    mvoted.live = False
                    await self.send_message(texts.client.KICK_FROM_TEMP_CAMP.format(user=mvoted.link))
                    if self.gameOverCheck() == Codes.GAME_OVER:
                        return Codes.GAME_OVER
                else:
                    await self.send_message("Разошлись во мнении")
                for player in self.players:
                    player.clearVote()
            self._round += 1

    async def start(self):
        self.connectTime = 1

    async def connectWaiter(self):
        while self.connectTime != 0:
            if self.connectTime % 30 == 0:
                self.messages['connectTimes'].append(await self.bot.send_message(self.id, f"Осталось {self.connectTime} секнд"))
            self.connectTime -= 1
            await sleep(1)
        for message in self.messages['connectTimes']:
            await message.delete()
        await self.messages['createMessage'].delete()
        if len(self.players) < 4:
            return Codes.NOT_HAVE_PLAYERS
        await self.send_message('Игра начинается')
        self.genBunker()
        await self.send_message(texts.client.GAME_RULES)
        return await self.mainloop()
