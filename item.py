
class Item:
    def __init__(self, name, stats:list[tuple], equip_type: int):
        self.name = name
        self.stat_effects = stats 
        self.equip = equip_type

    def get_stat_effects(self):
        return self.stat_effects

