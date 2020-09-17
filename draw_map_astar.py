from ways import graph
from ways import load_map_from_csv
import matplotlib.pyplot as plt
import utilities
from collections import namedtuple
import astar

def drawPath(path, color='b', roads = None):
    if(roads == None):
        roads = load_map_from_csv()
    flons, tolons, flats, tolats = [] ,[] ,[] ,[]
    plt.clf()
    for s, t in zip(path[:-1], path[1:]):
        ps, pt = roads[s], roads[t]
        flons.append(ps.lon)
        tolons.append(pt.lon)
        flats.append(ps.lat)
        tolats.append(pt.lat)
    
    plt.plot(flons, flats, tolons, tolats, color)

    fileName = 'solutions_img/'+ str(path[0]) + '_' + str(path[len(path)-1]) + '.png'
    plt.savefig(fileName, bbox_inches='tight')

roads = load_map_from_csv()
path = astar.find_astar_route(12530,12535, utilities.g,utilities.h,roads)

drawPath(path,'b',roads)    