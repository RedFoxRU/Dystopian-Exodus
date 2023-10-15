from  __future__ import annotations
from aiogram import types
import random
from typing import Text, Union
import typing
from aiogram import Bot
import keyboards
import texts.characters as characters
import texts

random.seed()


class Player():

    def __init__(self, id, bot: Bot, game:int,
                 full_name: typing.Text, username: typing.Text) -> None:
        self.username = username
        self.id = id
        self.game = game
        self.openMessage: types.Message = None
        self.full_name = full_name
        self.link = f'[{self.full_name}](tg://user?id={self.id})'
        self.body = random.randint(0, len(characters.body)-1) 
        self.sex = random.randint(0, 1)  # 0 - man, 1 -girl
        heal = random.randint(
            0, len(characters.heal)-1)
        self.heal = heal
        self.age = random.randint(11, 114)
        self.childFree = random.choices([True, False], [1,6])[0]
        self.phobia = random.randint(
            0, len(characters.phobias)-1)
        self.hobbys = random.randint(
            0, len(characters.hobbys)-1)
        self.utils = random.randint(
            0, len(characters.utils)-1)
        self.live = True
        self.bot = bot
        self.openedStats = []
        self.selected_to_open = None
        self.opened = {'sex':False, 'age': False, 'body': False,
                       'heal':False, 'phobia': False, 'hobby':False,
                       "utils": False, 'work': True
                       }
        self.voted = 0
        self.votedIn = 0

    async def send_message(self, text: Text,
                            parse_mode: typing.Optional[Text] = None,
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
                                            protect_content=protect_content,reply_to_message_id=reply_to_message_id,
                                            allow_sending_without_reply=allow_sending_without_reply,
                                            reply_markup=reply_markup)

    def voteIn(self, voteIn: Player):
        if voteIn.id != self.votedIn:
            self.votedIn = voteIn.id
            voteIn.voted += 1
    
    def getVoted(self):
        voted = ""
        if self.voted > 0:
            voted += str(self.voted)
        return voted
    
    def clearVote(self):
        self.voted = 0
        self.votedIn = 0

    def set_job(self, jobs: list) -> Text:
        self.job = random.randint(0, len(jobs)-1)
        return jobs[self.job]

    def change_sex(self):
        self.sex = random.randint(0, 1)  # 0 - man, 1 -girl

    def getAgeText(self) -> Text:
        return str(self.age)

    def getSexText(self) -> Text:
        sex = 'Мужской' if self.sex == 0 else 'Женский'
        sex += ' (Чайлдфри)' if self.childFree else ''
        return sex
    def getPhobiaText(self) -> Text:
        return ' - '.join([h for h in characters.phobias[self.phobia] if type(h)!=int])

    def getHealText(self) -> Text:
        return characters.heal[self.heal]

    def getHobbysText(self) -> Text:
        return characters.hobbys[self.hobbys]

    def getWorkText(self) -> Text:
        return characters.jobs[self.job]

    def getUtilsText(self) -> Text:
        return characters.utils[self.utils]

    def getBodyText(self) -> Text:
        return characters.body[self.body]

    async def send_stats(self):
        if self.live:
            self.openMessage = await self.send_message(texts.client.YOUR_STATS.format(age=self.getAgeText(), sex=self.getSexText(),
                                                        phobia=self.getPhobiaText(), heal=self.getHealText(),
                                                        hobbys=self.getHobbysText(), work=self.getWorkText(), 
                                                        utils=self.getUtilsText(), body=self.getBodyText(),opened=''),
                                                        reply_markup=keyboards.client.getInkbOpenStats(self.game, self.opened, self.selected_to_open))

    async def edit_opened_stats(self):
        await self.bot.edit_message_reply_markup(chat_id=self.openMessage.chat.id,
                                                message_id=self.openMessage.message_id,
                                                reply_markup=keyboards.client.getInkbOpenStats(self.game, self.opened, self.selected_to_open))

    def take_damage(self, damage: int):
        self.heal -= damage
        if self.heal <= 0:
            return 'die'
        else:
            return False

    def select_to_open(self, to_select = None ) -> bool: 
        self.selected_to_open = to_select
        return True

    def randomSelect(self):
        to_select = ['sex','age', 'body','hobby', 'heal', 'phobia', 'work', 'utils']
        for i in range(0, len(to_select)):
            rselect = random.choice(to_select)
            if not self.opened[rselect]:
                self.select_to_open(rselect)
                return True
            else:
                to_select.remove(rselect)
    

    def getOpenedText(self):
        username = f'@{self.username}'
        if self.opened['sex']:
            sex = 'Мужской' if self.sex == 0 else 'Женский'
            sex += ' Чайлдфри' if self.childFree else ''
        else:
            sex = '###'
        if self.opened['age']:
            age = self.age
        else:
            age = "###"
        if self.opened['body']:
            body = self.getBodyText()
        else:
            body = "###"
        if self.opened['hobby']:
            hobby = self.getHobbysText()
        else: 
            hobby = "###"
        if self.opened['heal']:
            heal = characters.heal[self.heal]
        else:
            heal = "###"
        if self.opened['phobia']:
            phobia = ' - '.join([h for h in characters.phobias[self.phobia] if type(h)!=int])
        else:
            phobia = "###"
        if self.opened['utils']:
            utils = characters.utils[self.utils]
        else:
            utils = "###"
        if self.opened['work']:
            work=characters.jobs[self.job]
        else:
            work = "###"
        return f"""Характеристики: {username}
Пол: {sex}
Возраст: {age}
Телосложение: {body}
Работа: {work}
Здоровье: {heal}
Фобия: {phobia}
Хобби: {hobby}
Факт: {utils}
"""

    async def send_opened_stats_to(self, id):
        await self.bot.send_message(chat_id=id, text=self.getOpenedText())

    async def open(self):
        if not self.live:
            return ''
        selected_to_open = ''
        if not self.selected_to_open:
            self.randomSelect()

        match self.selected_to_open:
            case 'sex':
                self.opened['sex'] = True
                selected_to_open = "пол:\n "
                selected_to_open += self.getSexText()
            case 'age':
                self.opened['age'] = True
                selected_to_open = "возраст:\n "
                selected_to_open += self.getAgeText()
            case 'body':
                self.opened['body'] = True
                selected_to_open = "телосложение:\n "
                selected_to_open += self.getBodyText()
            case 'heal':
                self.opened['heal'] = True
                selected_to_open = "здоровье:\n "
                selected_to_open += self.getHealText()
            case 'phobia':
                self.opened['phobia'] = True
                selected_to_open = "фобия:\n "
                selected_to_open += self.getPhobiaText()
            case 'hobby':
                self.opened['hobby'] = True
                selected_to_open = "хобби:\n "
                selected_to_open += self.getHobbysText()
            case 'utils':
                self.opened['utils'] = True
                selected_to_open = "дополнительный факт:\n "
                selected_to_open += self.getUtilsText()
            case 'work':
                self.opened['work'] = True
                selected_to_open = "профессия:\n "
                selected_to_open += self.getWorkText()
        self.selected_to_open = None
        return selected_to_open
