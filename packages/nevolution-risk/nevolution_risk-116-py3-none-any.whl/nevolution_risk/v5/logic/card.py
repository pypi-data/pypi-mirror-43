from random import randint

#from nevolution_risk.v3.logic import graph



class Card(object):

    def __init__(self):
        self.infantry = 1
        self.cavalry = 2
        self.artillery = 3

    def area_card(self):
        return randint(1, 3)

    #def area_map_reward(self):
    #    for continent in graph.continents:
    #        var = 0
    #        current_player = continent.nodes[0].player
    #        for node in continent.nodes:
    #            if node.player == current_player:
    #                var = var + 1
    #        if var == len(continent.nodes):
    #            self.area_card()

if __name__ == '__main__':
    pass