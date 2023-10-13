from hystory.generator import Generator
from player import *


if __name__ == "__main__":
    jobs = characters.jobs
    players = []
    for i in range(4):
        players.append(player.Player(i))
    
    for player_ in players:
        job = player_.set_job(jobs)
        jobs.remove(job)
    # print(players)
    mans = []
    girls = []
    for player_ in players:
        if player_.sex == 0:
            mans.append(player_)
        elif player_.sex == 1:
            girls.append(player_)
    i = 0
    while True:
        if len(mans) == 0:
            for player_ in players:
                player_.change_sex()
        if len(girls) == 0:
            for player_ in players:
                player_.change_sex()
        mans = []
        girls = []
        for player_ in players:
            if player_.sex == 0:
                mans.append(player_)
            elif player_.sex == 1:
                girls.append(player_)
        if len(girls) != 0 and len(mans) != 0:
            break
    # for i in range(0,10):
    generator = Generator(0, mans, girls, 2, 4, players)
    generator.gen()
    print(generator.hystory, "\n")
    print(generator.get_text())