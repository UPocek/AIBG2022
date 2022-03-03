from receive_DTO import *
from send_DTO import *

num_of_turn = 0


def not_occupied(tile, player):
    for t in player.tiles:
        return not (t.x == tile[0] and t.y == tile[1])


def what_is_near(tile, no, me, other):
    ok_tiles = []
    directions = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
    for d in directions:
        new = [tile[0] + d[0], tile[1] + d[1]]
        if 0 <= new[0] <= 7 and 0 <= new[1] <= 7 and not_occupied(new, me) and not_occupied(new, other) and new not in no:
            ok_tiles.append(new)
    return ok_tiles


class API:
    def __init__(self):
        self.dto = None
        self.matrix = [[None for i in range(8)] for j in range(8)]
        self.my_tiles = None
        self.num_special = 0
        self.num_tiles = 0
        self.tiles_available = None
        self.now_both = None
        self.predicted_tiles = 0

    def _what_is_mine(self):
        my_tiles = []
        for mt in self.dto.source.tiles:
            my_tiles.append((mt.x, mt.y))
        self.my_tiles = my_tiles
        self.num_tiles = len(self.my_tiles)
        self.tiles_available = my_tiles
        self.now_bought = []

    def _create_matrix(self):
        for title in self.dto.tiles:
            self.matrix[title.x][title.y] = {'x': title.x, 'y': title.y, 'isPlanted': title.bIsPlanted, 'isSpecial': title.bIsSpecial,
                                             'plant': title.plantDTO}

    def buy_best(self):
        available_to_buy = []
        diagonal = []
        for t in self.my_tiles:
            available_to_buy.extend(what_is_near(t, self.now_bought, self.dto.source, self.dto.enemy))
        for tile in self.dto.tiles:
            if tile.bIsSpecial:
                for a in available_to_buy:
                    if tile.x == a[0] and tile.y == a[1]:
                        return a
        for a in available_to_buy:
            if a[0] == a[1]:
                diagonal.append(a)
        if len(diagonal) > 0:
            return diagonal[0]
        elif len(available_to_buy) > 0:
            return available_to_buy[0]
        else:
            print("Nije mogao da pronadje ni jedan validan potez")
            # SAMOTEST
            exit()

    def plant_on_best(self):
        for tile in self.dto.tiles:
            if tile.bIsSpeciala:
                best = [tile.x, tile.y]
                if best in self.tiles_available:
                    self.tiles_available.remove(best)
                    return best
        best = self.tiles_available[0]
        self.tiles_available.remove(best)
        return best

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
    api._what_is_mine()
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
        return api.shop([(6, 1), (4, 2), (0, 1)])
    elif num_of_turn == 6:
        return api.plant([(6, 0, 0)])
    elif num_of_turn == 7:
        return api.water([(1, 0, 0)])
    elif num_of_turn == 8:
        return api.harvest()
    elif num_of_turn == 9:
        return api.buy_best()
    elif num_of_turn == 10:
        return api.plant(())

    return "{}"
