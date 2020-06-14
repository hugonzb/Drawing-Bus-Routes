import networkx as nx
import matplotlib.pyplot as plt
import sys
import re

# DrawingBusRoutes.py
# Etude 12
# Semester 1 2020
#
# Draws network of bus routes, highlights the shortest path
# and puts the output into a PDF file.
# 
# @author: Hugo Baird

def getCities(cities, lines):
    try:
        for line in lines: 
          splitLine = line.split(',')
          i=0 
          while i<2: 
            exists = "false"
            if splitLine[i] not in cities: 
                cities.append(splitLine[i].strip())
            i = i + 1
        return cities
    except:
        print("Invalid: route set")
        sys.exit(0)

if __name__ == '__main__':
        if sys.__stdin__.isatty():
            print('Invalid: No input')
            sys.exit(0)
        G = nx.Graph()
        destination = sys.stdin.readline()
        destSplit = destination.split(',')
        if len(destSplit) != 2 or destSplit[0].strip() == "" or destSplit[1].strip() == "":
            print("Invalid: route")
            sys.exit(0)
        lines = sys.stdin.readlines()   
        cities = [] 
        cities = getCities(cities, lines)
        uniqueEdges = []
        for city in cities:
            G.add_node(city.lower().strip())
        for line in lines:
            line = line.lower().strip()
            splitLine = line.split(',')
            firstLocation = splitLine[0].strip()
            secondLocation = splitLine[1].strip()
            weight = splitLine[2].strip()
            if len(splitLine) != 3 or firstLocation == "" or secondLocation == "" or weight == "" or bool(re.match('^[0-9\.]*$',weight)) == False:
                print("Invalid: route set")
                sys.exit(0)
            if (firstLocation + " " + secondLocation not in uniqueEdges):
                G.add_edge(firstLocation, secondLocation, weight=float(weight))
                uniqueEdges.append(firstLocation + " " + secondLocation)
            else:
                print("Invalid: Non-unique routes")
                sys.exit(0)

        shortest_path = nx.dijkstra_path(G, destSplit[0].lower().strip(), destSplit[1].lower().strip())
        node_list = []
        shortest_path_nodes = []
        edge_list = []
        shortest_path_edges = []
        matched = '0'

        labels = nx.get_edge_attributes(G, 'weight')
        for node in G:
            if node in shortest_path:
                shortest_path_nodes.append(node)
            else:
                node_list.append(node)

        for e in G.edges():
            for i in range(len(shortest_path)-1):
                if e == (shortest_path[i], shortest_path[i+1]) or  e == (shortest_path[i+1], shortest_path[i]): 
                    shortest_path_edges.append(e)
                    matched = '1'
            if (matched == '0'): 
                edge_list.append(e)
            matched = '0'

        pos = nx.spring_layout(G)


        nx.draw_networkx_nodes(G, pos, nodelist=node_list, node_size=500, node_color='blue', alpha=0.5)
        nx.draw_networkx_nodes(G, pos, nodelist=shortest_path_nodes, node_size=500, node_color='orange', alpha=0.8)
        nx.draw_networkx_edges(G, pos, width=2, edgelist=edge_list, edge_color='blue', style='dashed', alpha=0.5)
        nx.draw_networkx_edges(G, pos, width=2, edgelist=shortest_path_edges, edge_color='green', style='solid', alpha=1)
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edge_labels(G,pos, edge_labels=labels, font_weight='bold')

        plt.box(False)
        plt.title("Cheapest bus route - COSC326")
        plt.savefig("busroute.png")
