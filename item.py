
class Item:
    def __init__(self, name, stats:list[tuple], equip_type: int):
        self.name = name
        self.stat_effects = stats 
        self.equip = equip_type

    def get_stat_effects(self):
        return self.stat_effects



WEAPONS = {
    "Rusty Dagger": 1,
    "Iron Sword": 3,
    "Steel Blade": 5,
    "Flame Axe": 7,
    "Zayan's Bane": 10,
}
