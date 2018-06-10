import argparse
import os
import re
import sys
import time
import profile
import cProfile

# Command line arguments
parser=argparse.ArgumentParser(description='Calculate the shortest path between all pairs of vertices in a graph')
parser.add_argument('--algorithm',default='a',\
    help='Algorithm: Select the algorithm to run, default is all. (a)ll, (b)ellman-ford only or (f)loyd-warshall only')
parser.add_argument('-v','--verbose',action='store_true')
parser.add_argument('--profile',action='store_true')
parser.add_argument('filename',metavar='<filename>',help='Input file containing graph')

graphRE=re.compile("(\\d+)\\s(\\d+)")
edgeRE=re.compile("(\\d+)\\s(\\d+)\\s(-?\\d+)")

vertices=[]
edges=[]

def BellmanFord(G):
    pathPairs=[]
    d = G[1]
    
    for i in range(len(G[0])):
        d[i][i] = 0
            
    for x in range(len(G[0])):
        dist = []
        for i in range(len(G[0])):
            dist.append(float("inf"))
        dist[x] = 0
        for i in range(len(G[0])-1):
            for u in range(len(d)):
                for v in range(len(d)):
                    if dist[u] != float("inf") and float(dist[v]) > float(dist[u]) + float(d[u][v]):
                        print(float(dist[v]))
                        dist[v] = int(dist[u]) + int(d[u][v])
                        #dist[v] = str(dist[v])   

        for u in range(len(d)):
            for v in range(len(d)):
                if float(dist[v]) > float(dist[u]) + float(d[u][v]):
                    print("neg weight")
        pathPairs.append(dist)          
    # The pathPairs list will contain the 2D array of shortest paths between all pairs of vertices 
    # [[w(1,1),w(1,2),...]
    #  [w(2,1),w(2,2),...]
    #  [w(3,1),w(3,2),...]
    #   ...]
        # TODO: Fill in your Bellman-Ford algorithm here
    for i in pathPairs:
        print(i)

    print('BellmanFord algorithm is complete')
    return pathPairs

def FloydWarshall(G):
    pathPairs=[]
    d = G[1]
    for i in range(len(d)):
        d[i][i] = 0
        pathPairs.append(d[i])
    
    for i in range(len(G[0])):
        for k in range(len(G[0])):
            for j in range(len(G[0])):
                if float(pathPairs[k][j]) > float(pathPairs[k][i]) + float(pathPairs[i][j]):
                    print(float(pathPairs[k][j]))
                    #print(float(pathPairs[k][i]) + float(pathPairs[i][j]))
                    pathPairs[k][j] = int(pathPairs[k][i]) + int(pathPairs[i][j])
                    #pathPairs[k][j] = str(pathPairs[k][j])

    # TODO: Fill in your Floyd-Warshall algorithm here
    print('FloydWarshall algorithm is complete')
    # The pathPairs list will contain the 2D array of shortest paths between all pairs of vertices 
    # [[w(1,1),w(1,2),...]
    #  [w(2,1),w(2,2),...]
    #  [w(3,1),w(3,2),...]
    #   ...]
    return pathPairs

def readFile(filename):
    global vertices
    global edges
    # File format:
    # <# vertices> <# edges>
    # <s> <t> <weight>
    # ...
    inFile=open(filename,'r')
    line1=inFile.readline()
    graphMatch=graphRE.match(line1)
    if not graphMatch:
        print(line1+" not properly formatted")
        quit(1)
    vertices=list(range(int(graphMatch.group(1))))
    edges=[]
    for i in range(len(vertices)):
        row=[]
        for j in range(len(vertices)):
            row.append(float("inf"))
        edges.append(row)
    for line in inFile.readlines():
        line = line.strip()
        edgeMatch=edgeRE.match(line)
        if edgeMatch:
            source=edgeMatch.group(1)
            sink=edgeMatch.group(2)
            if int(source) > len(vertices) or int(sink) > len(vertices):
                print("Attempting to insert an edge between "+source+" and "+sink+" in a graph with "+vertices+" vertices")
                quit(1)
            weight=edgeMatch.group(3)
            edges[int(source)-1][int(sink)-1]=weight
    G = (vertices,edges)
    return (vertices,edges)

def matrixEquality(a,b):
    if len(a) == 0 or len(b) == 0 or len(a) != len(b): return False
    if len(a[0]) != len(b[0]): return False
    for i,row in enumerate(a):
        for j,value in enumerate(b):
            if a[i][j] != b[i][j]:
                return False
    return True


def main(filename,algorithm):
    G=readFile(filename)
    pathPairs = []
    # G is a tuple containing a list of the vertices, and a list of the edges
    # in the format ((source,sink),weight)
    if algorithm == 'b' or algorithm == 'B':
        # TODO: Insert timing code here
        cProfile.runctx('BellmanFord(G)', globals=globals(), locals=locals())
        pathPairs = BellmanFord(G)
    if algorithm == 'f' or algorithm == 'F':
        # TODO: Insert timing code here
        cProfile.runctx('FloydWarshall(G)', globals=globals(), locals=locals())
        pathPairs = FloydWarshall(G)
    if algorithm == 'a':
        print('running both') 
        pathPairsBellman = BellmanFord(G)
        pathPairsFloyd = FloydWarshall(G)
        pathPairs = pathPairsBellman
        if matrixEquality(pathPairsBellman,pathPairsFloyd):
            print('Floyd-Warshall and Bellman-Ford did not produce the same result')
    with open(os.path.splitext(filename)[0]+'_shortestPaths.txt','w') as f:
        for row in pathPairs:
            for weight in row:
                f.write(str(weight)+' ')
            f.write('\n')

if __name__ == '__main__':
    args=parser.parse_args()
    main(args.filename,args.algorithm)
