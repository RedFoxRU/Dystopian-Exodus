import random
from typing import Text
from player import characters

class Player():
    
    def __init__(self, id) -> None:
        self.id = id
        self.sex = random.randint(0,1) # 0 - man, 1 -girl
        self.age = random.randint(11,114)
        self.childFree = random.randint(0,1) # 0 - False, 1 - True
        self.phobia = characters.phobias[random.randint(0, len(characters.phobias)-1)]
        self.heal = characters.heal[random.randint(0, len(characters.heal)-1)]
        self.hobbys = characters.hobbys[random.randint(0, len(characters.hobbys)-1)]
        self.utils = characters.utils[random.randint(0, len(characters.utils)-1)]
        self.live = True
        if self.sex == 0: 
            self.heal = 6
        else:
            self.heal = 4

    def set_job(self, jobs) -> Text:
        self.job = jobs[random.randint(0, len(jobs)-1)]
        return self.job
    
    def change_sex(self):
        self.sex = random.randint(0,1) # 0 - man, 1 -girl
        if self.sex == 0: 
            self.heal = 6
        else:
            self.heal = 4
    def take_damage(self, damage):
        self.heal -= damage
        if self.heal <= 0:
            return 'die'
        else:
            return False
