from send_DTO import *

num_of_turn = 0


def not_occupied(tile, player):
    if len(player.tiles) <= 0:
        return True
    for t in player.tiles:
        if t.x == tile[0] and t.y == tile[1]:
            return False
    return True


def what_is_near(tile, no, me, other):
    ok_tiles = []
    directions = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
    for d in directions:
        new = (tile[0] + d[0], tile[1] + d[1])
        if 0 <= new[0] <= 7 and 0 <= new[1] <= 7 and not_occupied(new, me) and not_occupied(new, other) and new not in no:
            ok_tiles.append(new)
    return ok_tiles


# INTelligence - Tamara Ilic, Bojan Mijanovic, Uros Pocek
class API:
    def __init__(self):
        self.dto = None
        self.matrix = [[None for i in range(8)] for j in range(8)]
        self.my_tiles = None
        self.num_special = 0
        self.num_tiles = 0
        self.tiles_available = None
        self.now_bought = None
        self.last_bought = None
        self.what_strategy = 1

    def _what_is_mine(self):
        my_tiles = []
        self.num_special = 0
        for mt in self.dto.source.tiles:
            my_tiles.append((mt.x, mt.y))
            if mt.bIsSpecial:
                self.num_special += 1
        self.my_tiles = my_tiles
        self.num_tiles = len(self.my_tiles)
        self.tiles_available = my_tiles
        self.now_bought = []

    def what_to_water(self):
        tiles = []
        for tile in self.dto.source.tiles:
            if tile.bIsPlanted:
                tiles.append((tile.plantDTO.waterNeeded, tile.x, tile.y))
        return tiles

    def attack_best(self):
        diagonal = []
        all = []
        for tile in self.dto.enemy.tiles:
            best = (tile.x, tile.y)
            if tile.bIsSpecial:
                return best
            elif tile.x == tile.y:
                diagonal.append(best)
            else:
                all.append(best)
        if len(diagonal) > 0:
            return diagonal[-1]
        return all[0]

    def buy_best(self, all=False):
        available_to_buy = []
        diagonal = []
        for t in self.my_tiles:
            win = what_is_near(t, self.now_bought, self.dto.source, self.dto.enemy)
            for w in win:
                if w not in available_to_buy:
                    available_to_buy.append(w)
        if all:
            return available_to_buy
        for tile in self.dto.tiles:
            if tile.bIsSpecial:
                for a in available_to_buy:
                    if tile.x == a[0] and tile.y == a[1]:
                        self.now_bought.append(a)
                        return a
        for a in available_to_buy:
            if a[0] == a[1]:
                diagonal.append(a)
        if len(diagonal) > 0:
            self.now_bought.append(diagonal[0])
            return diagonal[0]
        elif len(available_to_buy) > 0:
            x = available_to_buy.pop()
            self.now_bought.append(x)
            return x
        else:
            return [0, 0]

    def plant_on_best(self):
        for tile in self.dto.tiles:
            if tile.bIsSpecial:
                best = (tile.x, tile.y)
                if best in self.tiles_available:
                    self.tiles_available.remove(best)
                    return best
        try:
            best = self.tiles_available[0]
            self.tiles_available.remove(best)
        except Exception:
            best = [0, 0]
        return best

    def buy_best_flower(self, money):
        cards = {6: [3800, 1],
                 5: [2000, 5],
                 4: [900, 2],
                 3: [900, 2]}
        buy = {0: 0}
        for field in self.my_tiles:
            for key in cards:
                if money - cards[key][0] >= 0:
                    if key in buy:
                        buy[key] += 1
                        buy[0] += cards[key][1]
                    else:
                        buy[key] = 1
                        buy[0] += cards[key][1]
                    money -= cards[key][0]
                    break
        return buy

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


def bot_input(dto):
    # Shop(id,amount)
    # 0 : Water
    # 1 : Krtica
    # 2 : Djubrivo
    # 3 : Anemone
    # 4 : BlueJazz
    # 5 : Crocus
    # 6 : Tulip

    # Final_Version
    global num_of_turn
    api.dto = dto
    api._what_is_mine()
    num_of_turn += 1

    uros = False
    we_hope = [(0, 1), (1, 1), (1, 0)]
    for tt in api.dto.tiles:
        new_tt = (tt.x, tt.y)
        if new_tt in we_hope and tt.bIsSpecial:
            uros = True
            break

    if uros:
        api.what_strategy = 2
    else:
        api.what_strategy = 1

    if api.what_strategy == 2:

        if num_of_turn == 1:
            return api.shop([(0, 1), (6, 1)])
        elif num_of_turn == 2:
            return api.plant([(6, *api.plant_on_best())])
        elif num_of_turn == 3:
            what_to_water = api.what_to_water()
            return api.water(what_to_water)
        elif num_of_turn == 4:
            return api.harvest()
        elif num_of_turn == 5:
            return api.shop([(6, 1), (0, 1)])
        elif num_of_turn == 6:
            return api.plant([(6, *api.plant_on_best())])
        elif num_of_turn == 7:
            what_to_water = api.what_to_water()
            return api.water(what_to_water)
        elif num_of_turn == 8:
            change_s = False
            for tile in api.dto.enemy.tiles:
                if tile.bIsSpecial:
                    change_s = True
                    break
            if change_s:
                api.what_strategy = 1
            return api.harvest()
        elif num_of_turn == 9:
            return api.shop([(1, 1)])
        elif num_of_turn == 10:
            return api.mole([api.attack_best()])
        elif num_of_turn == 11:
            a = []
            money = api.dto.source.gold
            what_to_buy = api.buy_best_flower(money)
            api.last_bought = what_to_buy
            for key, value in what_to_buy.items():
                a.append((key, value))
            return api.shop(a)
        elif num_of_turn == 12:
            a = []
            what_to_plant = api.last_bought
            del what_to_plant[0]
            for key in what_to_plant:
                for i in range(what_to_plant[key]):
                    a.append((key, *api.plant_on_best()))
            return api.plant(a)
        elif num_of_turn == 13:
            what_to_water = api.what_to_water()
            return api.water(what_to_water)
        elif num_of_turn == 14:
            return api.harvest()
        elif num_of_turn == 15:
            a = []
            money = api.dto.source.gold
            if len(api.dto.enemy.tiles) > 0:
                if money >= 10000:
                    a.append((1, 1))
                    money -= 10000
            what_else_to_buy = api.buy_best_flower(money)
            api.last_bought = what_else_to_buy
            for key, value in what_else_to_buy.items():
                a.append((key, value))
            return api.shop(a)
        elif num_of_turn == 16:
            if len(api.dto.enemy.tiles) > 0:
                return api.mole([api.attack_best()])
            else:
                try:
                    return api.land(api.buy_best(True))
                except Exception:
                    return api.harvest()
        elif num_of_turn == 17:
            a = []
            what_to_plant = api.last_bought
            del what_to_plant[0]
            for key in what_to_plant:
                for i in range(what_to_plant[key]):
                    a.append((key, *api.plant_on_best()))
            return api.plant(a)
        elif num_of_turn == 18:
            what_to_water = api.what_to_water()
            return api.water(what_to_water)
        elif num_of_turn == 19:
            num_of_turn = 14
            return api.harvest()

    else:

        if num_of_turn == 1:
            return api.shop([(0, 1), (6, 1)])
        elif num_of_turn == 2:
            x, y = api.plant_on_best()
            return api.plant([(6, x, y)])
        elif num_of_turn == 3:
            tiles = []
            for tile in api.dto.source.tiles:
                if tile.bIsPlanted:
                    tiles.append((tile.plantDTO.waterNeeded, tile.x, tile.y))
            return api.water(tiles)
        elif num_of_turn == 4:
            return api.harvest()
        elif num_of_turn == 5:
            return api.shop([(6, 2), (0, 4), (4, 1)])
        elif num_of_turn == 6:
            x, y = api.plant_on_best()
            return api.plant([(6, x, y)])
        elif num_of_turn == 7:
            tiles = []
            for tile in api.dto.source.tiles:
                if tile.bIsPlanted:
                    tiles.append((tile.plantDTO.waterNeeded, tile.x, tile.y))
            return api.water(tiles)
        elif num_of_turn == 8:
            return api.harvest()
        elif num_of_turn == 9:
            return api.land([api.buy_best()])
        elif num_of_turn == 10:
            x, y = api.plant_on_best()
            x1, y1 = api.plant_on_best()
            return api.plant([(6, x, y), (4, x1, y1)])
        elif num_of_turn == 11:
            tiles = []
            for tile in api.dto.source.tiles:
                if tile.bIsPlanted:
                    tiles.append((tile.plantDTO.waterNeeded, tile.x, tile.y))
            return api.water(tiles)
        elif num_of_turn == 12:
            return api.harvest()
        else:
            if num_of_turn % 5 == 3:
                num_of_tulip = 0
                num_of_jazz = 0
                num_of_moles = 0
                for card in dto.source.cards:
                    if card.cardId == 1:
                        num_of_moles = card.owned
                if dto.source.gold > 10000 and num_of_moles == 0:
                    money = dto.source.gold - 10000
                else:
                    money = dto.source.gold
                if len(dto.source.tiles) <= money // 3800:
                    num_of_tulip = len(dto.source.tiles)
                else:
                    num_of_tulip = money // 3800
                money_left = money - num_of_tulip * 3800
                if len(dto.source.tiles) - num_of_tulip <= money_left // 900:
                    num_of_jazz = len(dto.source.tiles) - num_of_tulip
                else:
                    num_of_jazz = money_left // 900

                return api.shop([(1, 1 - num_of_moles), (6, num_of_tulip), (4, num_of_jazz), (0, num_of_tulip + num_of_jazz * 2)])
            elif num_of_turn % 5 == 4:
                if len(dto.enemy.tiles) > 0:
                    polje = api.attack_best()
                    return api.mole([(polje[0], polje[1])])
                else:
                    land = api.buy_best(True)
                    return api.land(land)
            elif num_of_turn % 5 == 0:
                list = []
                dto.source.cards = sorted(dto.source.cards, key=lambda x: x.cardId, reverse=True)
                for card in dto.source.cards:
                    if card.cardId in [3, 4, 5, 6]:
                        for i in range(card.owned):
                            x, y = api.plant_on_best()
                            list.append((card.cardId, x, y))
                return api.plant(list)
            elif num_of_turn % 5 == 1:
                tiles = []
                for tile in api.dto.source.tiles:
                    if tile.bIsPlanted:
                        tiles.append((tile.plantDTO.waterNeeded, tile.x, tile.y))
                return api.water(tiles)
            elif num_of_turn % 5 == 2:
                return api.harvest()

    return "{}"
