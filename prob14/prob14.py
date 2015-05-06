import tarjan #https://github.com/bwesterb/py-tarjan

def point_inside_polygon(x, y, vertices):
    point = (x,y)
    previous_side = None
    nv = len(vertices)
    for i in xrange(nv):
        v1 = vertices[i]
        j = i + 1 if i < nv - 1 else 0
        v2 = vertices[j]
        affine_segment = v_sub(v2, v1)
        affine_point = v_sub(point, v1)
        current_side = get_side(affine_segment, affine_point)
        if current_side == 0:
            return True #point is on the edge
        if current_side is None:
            return False #outside the edge
        elif previous_side is None: #first segment
            previous_side = current_side
        elif previous_side != current_side:
            return False
    return True

def get_side(edge, point):
    x = x_product(edge, point)
    if x < 0:
        return -1
    elif x > 0:
        return +1
    else:
        ip = inner_product(edge, point)
        norm2 = inner_product(edge, edge)
        if ip < 0 or ip > norm2:
            return None
        else:
            return 0

def v_sub(a, b):
    return (a[0]-b[0], a[1]-b[1])

def inner_product(a, b):
    return a[0]*b[0]+a[1]*b[1]

def x_product(a, b):
    return a[0]*b[1]-a[1]*b[0]

#get input
E = int(raw_input())
ships = []
for ship in xrange(E):
    x,y  = map(int, raw_input().split())
    v = int(raw_input())
    verts = map(int, raw_input().split())
    verts = [(verts[2*i],verts[2*i+1]) for i in xrange(v)]
    ships.append((x,y,tuple(verts)))


#build the graph where edge i -> j means ship j is inside the explosion
#shape of ship i
graph = {}
rev_graph = [set() for i in xrange(E)]
for ship1 in xrange(E):
    graph[ship1] = []
    for ship2 in xrange(E):
        if ship2 == ship1:
            continue
        if point_inside_polygon(ships[ship2][0], ships[ship2][1], ships[ship1][2]):
            graph[ship1].append(ship2)
            rev_graph[ship2].add(ship1)

#find the strongly connected components of the graph
scc = [set(component) for component in tarjan.tarjan(graph)]


#the number of strongly connected components without incident edges
#from other scc's is the number of times we need to use little doctor
roots_of_condensed_graph = 0
for comp in xrange(len(scc)):
    component_has_outside_incident_edges = False
    for ship in scc[comp]:
        if rev_graph[ship] - scc[comp]:
            component_has_outside_incident_edges = True
            break
    if component_has_outside_incident_edges:
        continue
    roots_of_condensed_graph += 1

print roots_of_condensed_graph

