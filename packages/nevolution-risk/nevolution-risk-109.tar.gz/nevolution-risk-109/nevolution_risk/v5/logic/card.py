from random import randint

from nevolution_risk.v3.logic import Graph


class Card(object):

    def __init__(self):
        self.infantry = 1
        self.cavalry = 2
        self.artillery = 3

    def area_map(self, player):
        card = randint(1, 3)
        graph.players[player].area_maps.append(card)

    def area_map_reward(self, node):
        infa = graph.players[player].area_maps.count(self.infantry)
        cava = graph.players[player].area_maps.count(self.cavalry)
        arti = graph.players[player].area_maps.count(self.artillery)

        if infa >= 3:
            if graph.nodes[node].troops <= 4:
                graph.nodes[node].troops = graph.nodes[node].troops + 1
                for elem in graph.players[player].area_maps[:]:
                    if elem == self.infantry:
                        graph.players[player].area_maps.remove(elem)
        elif cava >= 3:
            if graph.nodes[node].troops <= 3:
                graph.nodes[node].troops = graph.nodes[node].troops + 2
                for elem in graph.players[player].area_maps[:]:
                    if elem == self.cavalry:
                        graph.players[player].area_maps.remove(elem)
        elif arti >= 3:
            if graph.nodes[node].troops <= 2:
                graph.nodes[node].troops = graph.nodes[node].troops + 3
                for elem in graph.players[player].area_maps[:]:
                    if elem == self.artillery:
                        graph.players[player].area_maps.remove(elem)
        elif infa >= 1 and cava >= 1 and arti >= 1:
            if graph.nodes[node].troops <= 4:
                graph.nodes[node].troops = graph.nodes[node].troops + 1
                graph.players[player].area_maps.remove(self.infantry)
                graph.players[player].area_maps.remove(self.cavalry)
                graph.players[player].area_maps.remove(self.artillery)

        # if len(graph.players[player].area_maps) % 3 == 0:
        #    if graph.nodes[node].troops <= 4:
        #        graph.nodes[node].troops = graph.nodes[node].troops + 1


if __name__ == '__main__':
    graph = Graph((1, 8), 2)
    player = 1

    cards = Card()

    graph.nodes[1].troops = 1
    print(graph.nodes[1].troops, "before reward")

    cards.area_map(player)
    cards.area_map(player)
    cards.area_map(player)

    print(graph.players[player].area_maps)

    cards.area_map_reward(1)
    print(graph.nodes[1].troops, "after reward")

    print(graph.players[player].area_maps)
