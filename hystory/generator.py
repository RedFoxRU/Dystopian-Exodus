import random
from texts import hystory_generate as hg

class Generator():
    
    def __init__(self, places, mans, girls, food, water, players ):
        self.places = places
        self.mans = mans
        self.girls = girls
        self.players = players
        self.food = food
        self.water = water
        self.hystory = ''
        self.text = ""

    def gen(self):
        self.hystory += str(random.randint(0, len(hg.catastrophe)-1))+"_" #catastrophe
        for i in range(0,12):
            x = random.randint(0,1)
            if x == 0:
                event = str(random.randint(0, len(hg.situations)-1))
                mounth_hystory = f's{event}'
                if event == "2":
                    players = random.sample(self.players, 1)
                    mounth_hystory+=f';{players[0].id}'
                    if random.randint(0,1) == 1:
                        mounth_hystory += 'd'
                    else:
                        mounth_hystory += 'l'
                self.hystory += f'{i}.{mounth_hystory}_'
            elif x == 1:
                event = str(random.randint(0, len(hg.events)-1))
                mounth_hystory = f'e{event}'
                if event == "3":
                    players = random.sample(self.players, 2)
                    mounth_hystory+=f';{players[0].id}|{players[1].id}'
                    if random.randint(0,1) == 1:
                        mounth_hystory += 'd'
                    else:
                        mounth_hystory += 'l'
                self.hystory += f'{i}.{mounth_hystory}_'
                
    def get_text(self):
        hystory = self.hystory.split('_')
        for i in range(1, len(hystory)):
            hystory[i] = hystory[i].split('.')
        self.text = f"Наши бравые {len(self.players)} молодцов входят в бункер из-за {hg.catastrophe[int(hystory[0])]}\n\n{hg.catastrophe_descript[int(hystory[0])]}\n"
        for i in range(1, len(hystory)-1):
            if hystory[i][1][0] == 's':
                if hystory[i][1][1] == '0':
                    self.text += f'Спустя {i} месяцев *Ничего*'
                elif hystory[i][1][1] == '1':
                    player = random.sample(self.players, 1)[0]
                    damage = random.randint(0,2)
                    self.text += f'Спустя {i} месяцев *Нехватка еды*'
                    if player.take_damage(damage) == 'die':
                        self.text += f", player_{player.id} не ел так давно, что умер"
                    else:
                        if damage == 0:
                            self.text += ", но она была незначительной, никто не пострадал"
                        elif damage == 1:
                            self.text += f", она была легкой, в ходе чего у player_{player.id} развилась Кахексия"
                        elif damage == 2:
                            self.text += f", она была легкой, в ходе чего у player_{player.id} развилась Алиментарная дистрофия"
                elif hystory[i][1][1] == '2':
                    player = random.sample(self.players, 1)[0]
                    damage = random.randint(0,2)
                    self.text += f'Спустя {i} месяцев *Нехватка воды*'
                    if player.take_damage(damage) == 'die':
                        self.text += f", player_{player.id} не пил воду так давно, что умер"
                    else:
                        if damage == 0:
                            self.text += ", но она была незначительной, никто не пострадал"
                        elif damage == 1:
                            self.text += f", она была легкой, в ходе чего у player_{player.id} началаось Обезвоживание"
                        elif damage == 2:
                            self.text += f", она была легкой, в ходе чего у player_{player.id} развилась Гиповолемия"
            self.text += '\n'
                    
        return self.text