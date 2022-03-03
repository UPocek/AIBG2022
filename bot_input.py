from receive_DTO import *
from send_DTO import *

num_of_turn = 0


class API:
    def __init__(self):
        self.dto = None
        self.matrix = [[None for i in range(8)] for j in range(8)]

    def _create_matrix(self):
        for title in self.dto.tiles:
            self.matrix[title.x][title.y] = {'x': title.x, 'y': title.y, 'isPlanted': title.bIsPlanted, 'isSpecial': title.bIsSpecial,
                                             'plant': title.plantDTO}

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
                actions.append(Action(cardid=item[0], amount=item[1]))
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


api = API()


def heuristic(dto):
    pass


def bot_input(dto):
    # Shop(id,amount)
    # 0 : Water
    # 1 : Krtica
    # 2 : Djubrivo
    # 3 : Anemone
    # 4 : BlueJazz
    # 5 : Crocus
    # 6 : Tulip

    global num_of_turn
    api.dto = dto
    api._create_matrix()
    num_of_turn += 1
    if num_of_turn == 1:
        return api.shop([(0, 1), (6, 1)])
    elif num_of_turn == 2:
        return api.plant([(6, 0, 0)])
    elif num_of_turn == 3:
        return api.water([(1, 0, 0)])
    elif num_of_turn == 4:
        return api.harvest()
    elif num_of_turn == 5:
        return api.shop([(0, 1), (6, 1)])

    return "{}"
