import json
#### DTO Classes
class Plant:
    def __init__(self, plantId, goldWorth, waterNeeded):
        self.plantId = plantId
        self.goldWorth = goldWorth
        self.waterNeeded = waterNeeded
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)
    
    def _get_name_from_id(self):
        if(self.plantId == 3):
            return 'ANEMONE_FLOWER'
        elif(self.plantId == 4):
            return 'BLUE_JAZZ'
        elif(self.plantId == 5):
            return 'CROCUS_FLOWER'
        elif(self.plantId == 6):
            return 'TULIP'
        return 'None'
    def __str__(self) -> str:
        return '\n\t\t{}, GoldWorth = {}, Water needed = {}\n'.format(self._get_name_from_id(), str(self.goldWorth),  str(self.waterNeeded))
class Tile:
    def __init__(self, x, y, bIsPlanted, bIsSpecial, plantDTO):
        self.x = x
        self.y = y
        self.bIsPlanted = bIsPlanted
        self.bIsSpecial = bIsSpecial
        self.plantDTO = plantDTO

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)
        self.plantDTO = Plant(self.plantDTO)
    
    def __str__(self) -> str:
       return '\n\tCoordinations = [{},{}], planted ={}, Special tile = {} {}\n'.format(str(self.x),str(self.y),str(self.bIsPlanted),str(self.bIsSpecial),self.plantDTO.__str__())

class Card:
    def __init__(self, cardId, owned):
        self.cardId = cardId
        self.owned = owned
    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)

    def _get_name_from_id(self):
        if(self.cardId == 0):
            return 'WATER_CARD'
        elif(self.cardId == 1):
            return 'MOLE_CARD'
        elif(self.cardId == 2):
            return 'FERTILIZER_CARD'
        elif(self.cardId == 3):
            return 'ANEMONE_FLOWERR_CARD'
        elif(self.cardId == 4):
            return 'BLUE_JAZZR_CARD'
        elif(self.cardId == 5):
            return 'CROCUS_FLOWERR_CARD'
        elif(self.cardId == 6):
            return 'TULIPR_CARD'
        return ''
    def __str__(self) -> str:
        return '\n\tOwned ' + str(self.owned) + ' ' + self._get_name_from_id()
class Player:
    def __init__(self,points,gold,fertilizerActive,tiles,cards):
        self.points = points
        self.gold = gold
        self.fertilizerActive = fertilizerActive
        self.tiles = tiles
        self.cards = cards

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)
        Tiles = []
        for tile in self.tiles:
            Tiles.append(Tile(tile))
        self.tiles = Tiles
        Cards = []
        for card in self.cards:
            Cards.append(Card(card))
        self.cards = Cards
    def __str__(self):
        tiles_str = ''
        cards_str = ''
        for tile in self.tiles: 
            tiles_str += str(tile)
        for card in self.cards:
            cards_str += str(card)
        return '\nGold = {}, Points = {} Fertilizer active for {} turns {} {}\n'.format(str(self.gold),str(self.points),str(self.fertilizerActive),tiles_str,cards_str)
class DTO:
    def __init__(self, tiles, source, enemy,daysTillRain):
        self.tiles = tiles
        self.source = source
        self.enemy = enemy
        self.daysTillRain = daysTillRain

    @classmethod
    def from_json(cls,json_string):
        json_dict = json.loads(json_string)
        obj = cls(**json_dict)
        obj.tiles = cls.tiles_dict_to_list(obj.tiles)
        obj.source = Player(obj.source)
        obj.enemy = Player(obj.enemy)
        return obj
    
    @classmethod
    def tiles_dict_to_list(cls,tiles):
        tiles_obj = []
        for tile in tiles:
            tiles_obj.append(Tile(tile))
        return tiles_obj
        

    def __str__(self):
        tiles_str = ''
        for tile in self.tiles:
            tiles_str += str(tile)
        return "Tiles = " + str(tiles_str) + "\nMy info = \n" + self.source.__str__() + "\nEnemy info = \n" + self.enemy.__str__() + "Days till rain = " + str(self.daysTillRain)
