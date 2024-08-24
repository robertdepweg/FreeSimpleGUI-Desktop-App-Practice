"""Beverage data models"""

# System Imports.
import os


class Beverage:
    """Beverage class"""

    def __init__(self, id, name, pack, price, active):
        """Constructor"""
        self.id = id
        self.name = name
        self.pack = pack
        self.price = price
        self.active = active

    def __str__(self):
        """String method"""
        active = "True" if self.active else "False"
        return f"| {self.id:>6} | {self.name:<56} | {self.pack:<15} | {self.price:>6.2f} | {active:<6} |"


class BeverageCollection:
    """BeverageCollection class"""

    def __init__(self):
        """Constructor"""
        self.beverages = []

    def __str__(self):
        """String method"""
        return_string = ""
        for beverage in self.beverages:
            return_string += f"{beverage}{os.linesep}"
        return return_string

    def add(self, id, name, pack, price, active):
        """Add a new beverage to the collection"""
        self.beverages.append(Beverage(id, name, pack, price, active))

    def find_by_id(self, id):
        """Find a beverage by it's id"""
        for beverage in self.beverages:
            if beverage.id == id:
                return beverage
