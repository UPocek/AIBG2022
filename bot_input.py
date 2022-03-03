import json
import requests
from receive_DTO import *
from send_DTO import *
num_of_turn = 0

class API:
    def __init__(self, player, opponent):
        self.player = player
        self.opponent = opponent

    def water(self, list):
        actions = []
        for item in list:
            actions.append(Action(amount=item[0], x=item[1], y=item[2]))
        return InputAction("W", actions).toJSON()

    def land(self, list):
        actions = []
        for item in list:
            actions.append(Action(x=item[0], y=item[1]))
        return InputAction("L", actions).toJSON()

    def plant(self, list):
        actions = []
        for item in list:
            if item[0] in [3, 4, 5, 6]:
                actions.append(Action(cardid=item[0], x=item[1], y=item[2]))
            else:
                print("Nije dobar id biljke")
        return InputAction("P", actions).toJSON()

    def shop(self, list):
        actions = []
        for item in list:
            if item[1] > 0 and 6 >= item[0] >= 0:
                actions.append(Action(x=0, y=0, cardid=item[0], amount=item[1]))
        return InputAction("C", actions).toJSON()

    def fertilizer(self, ):
        return InputAction("F", []).toJSON()

    def mole(self, list):
        actions = []
        for item in list:
            actions.append(Action(x=item[0], y=item[1]))
        return InputAction("M", actions).toJSON()

    def harvest(self):
        return InputAction("H", []).toJSON()



api = API(None, None)

def heuristic(dto):
    pass


def bot_input(dto):
    global num_of_turn
    print(dto)
    api.player = dto.source
    api.opponent = dto.enemy
    if num_of_turn < 9:
        if num_of_turn % 4 == 1:
            num_of_turn += 1
            return api.shop([(0, 1), (6, 1)])
            # return InputAction('C', [Action(0, 0, 0, 1), Action(0, 0, 6, 1)]).toJSON()
        elif num_of_turn % 4 == 2:
            num_of_turn += 1
            return api.plant([(6, 0, 0)])
            # return InputAction('P', [Action(cardid=6, x=0, y=0)]).toJSON()
        elif num_of_turn % 4 == 3:
            num_of_turn += 1
            return api.water([(1, 0, 0)])
        elif num_of_turn % 4 == 0:
            num_of_turn += 1
            return api.harvest()
            # return InputAction('H', [Action(x=0, y=0)]).toJSON()

    return "{}"