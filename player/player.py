import random
from typing import Text
from player import characters

class Player():
    
    def __init__(self) -> None:
        self.sex = random.randint(0,1) # 0 - man, 1 -girl
        self.age = random.randint(11,114)
        self.childFree = random.randint(0,1) # 0 - False, 1 - True
        self.phobia = characters.phobias[random.randint(0, len(characters.phobias)-1)]


    def set_job(self, jobs) -> Text:
        self.job = jobs[random.randint(0, len(jobs)-1)]
        return self.job