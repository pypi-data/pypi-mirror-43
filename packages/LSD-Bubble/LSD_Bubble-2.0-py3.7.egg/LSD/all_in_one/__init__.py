from math import inf
from LSD.filter import Filter


WHITE = 0
"""COLOR Definition Unseen"""
GREY = 1
"""COLOR Definition Toposort seen"""
BLACK = 2
"""COLOR Definition Finished vertex"""
GREEN = 3
"""COLOR Definition Seen but not finished"""
YELLOW = 4
"""COLOR Definition Dead end"""
# PURPLE = 5
"""COLOR Definition Part of a cycle"""
ORANGE = 5
"""COLOR Definition Seen in a path search"""
RED = 6
"""COLOR Definition Seen in a path search"""


def abitarry_graph_detect(graph, rep):
    g = ColordGraph(graph)
    for v in g.nodes:
        g.set_color(v, WHITE)
    for v, cycle in generate_starts(g):
        order, v2 = create_dfs_order(v, g, cycle)
        superbubble(g, order, SCCFilter(rep, v, v2), v, v2)


def generate_starts(g):
    for v in g.nodes:
        if g.get_color(v) == WHITE:
            if g.in_degree(v) == 0:
                yield v, False
    
    for cycle in find_cycles(g):
        # paths = find_paths(g, cycle)
        # cut = cycle[find_cover_cut(paths)]
        # yield cut,
        cover, value = find_paths(g, cycle)
        if cover:
            yield cycle[value], False
        else:
            paths = value
            cutpoint, position = find_cover_cut(paths)
            if cutpoint:
                yield cycle[position], True
            else:
                yield cycle[position], False


def find_cycles(g):
    for v in g.nodes:
        if g.get_color(v) == WHITE:
            stack = [v]
            while stack:
                u = stack[-1]
                c = g.get_color(u)
                if c == WHITE:
                    g.set_color(u, GREEN)
                    for w in g.successors(u):
                        wc = g.get_color(w)
                        if wc == WHITE:
                            stack.append(w)
                        elif wc == GREEN:
                            cycle = []
                            while stack[-1] != w:
                                x = stack.pop()
                                if g.get_color(x) == GREEN:
                                    cycle.append(x)
                                    # g.set_color(x, PURPLE)
                            # g.set_color(w, PURPLE)
                            cycle.append(stack.pop())
                            yield hashed_list(reversed(cycle))
                            break
                else:
                    if c == GREEN:
                        g.set_color(u, YELLOW)
                    stack.pop()


def cycle_distance(k, i, end):
    if end > i:
        return end - i - 1
    return end + k - i - 1


def create_tree(g, c, cycle):
    postorder = hashed_list()
    inorder = hashed_list()
    #Add cycle vertex as first in preorder
    inorder.append(c)
    stack = [c]
    #Keep purlple cycle vertex intact
    # for child in g.successors(c):
    #     if g.get_color(child) not in [BLACK, RED, PURPLE]:
    #         stack.append(child)
    #Create tree
    while stack:
        top = stack[-1]
        color = g.get_color(top)
        if color != ORANGE:
            g.set_color(top, ORANGE)
            #New vertex found
            inorder.append(top)
            for child in g.successors(top):
                #No backedge or finished vertex or cycle vertex
                if g.get_color(child) not in [BLACK, ORANGE, RED] and child not in cycle:
                    stack.append(child)
        #Is already orange and so finished now
        else:
            #When not already finished
            if top not in postorder:
                #Add postorder
                postorder.append(top)
            #Remove from stack
            stack.pop()
    #Add cycle vertex as last in postorder
    # postorder.append(c)
    return postorder, inorder


def caculate_cmax(g, cycle, postorder, inorder, i):
    k = len(cycle)
    def cycle_min(*args):
        min_value = inf
        min_position = None
        for x in args:
            new_value = cycle_distance(k, i, x)
            if new_value < min_value:
                min_value = new_value
                min_position = x
        return min_position
    
    def cycle_max(*args):
        max_value = -1
        max_position = None
        for x in args:
            new_value = cycle_distance(k, i, x)
            if new_value > max_value:
                max_value = new_value
                max_position = x
        return max_position

    def checkbackedge(v, u):
        return postorder.index(v) < postorder.index(u)
    
    for j in range(len(postorder)):
        v = postorder[j]
        inpos = inorder.index(v)
        g.property(v, "link", inpos)
        for child in g.successors(v):
            color = g.get_color(child)
            # Is in cycle
            if child in cycle:
                pos = cycle.index(child)
                g.update_property(v, "min", cycle_min, pos)
                g.update_property(v, "max", cycle_max, pos)
            # Do nothing when in other run complete finished
            elif color != BLACK:
                # Is back edge
                if color != RED and checkbackedge(v, child):
                    g.update_property(v, "link", min, inorder.index(child))
                # Is no back edge
                else:
                    # look for one vertex cover
                    if g.property(child, "min") is not None and \
                            cycle_distance(k, i, g.property(child, "min")) > cycle_distance(k, i, g.property(child, "max")):
                        return True, g.property(child, "min")
                    # Update values
                    g.update_property(v, "min", cycle_min, g.property(child, "min"))
                    g.update_property(v, "max", cycle_max, g.property(child, "max"))
                    # If not finished
                    if color != RED:
                        g.update_property(v, "link", min, g.property(child, "link"))
        # Finished subtree
        if g.property(v, "link") == inpos:
            finish_subtree(g, v)
    return False, g.property(cycle[i], "max")
    

def finish_subtree(g, v):
    minval = g.property(v, "min")
    maxval = g.property(v, "max")
    nexts = [v]
    while nexts:
        u = nexts.pop()
        g.set_color(u, RED)
        g.property(u, "min", minval)
        g.property(u, "max", maxval)
        
        for w in g.successors(u):
            if g.get_color(w) == ORANGE:
                nexts.append(w)
                


def find_paths(g, cycle):
    ret = []
    for i in range(len(cycle)):
        c = cycle[i]
        postorder, inorder = create_tree(g, c, cycle)
        cover, value = caculate_cmax(g, cycle, postorder, inorder, i)
        if cover:
            return True, value
        ret.append(value)
    return False, ret

# def find_paths(g, cycle):
#     revers = {}
#     for i in range(len(cycle)):
#         revers[cycle[i]] = i
#     k = len(cycle)
#     ret = []
#     for i in range(len(cycle)):
#         v = cycle[i]
#
#         def cycle_min(*args):
#             min_value = inf
#             min_position = None
#             for x in args:
#                 new_value = cycle_distance(k, i, x)
#                 if new_value < min_value:
#                     min_value = new_value
#                     min_position = x
#             return min_position
#
#         def cycle_max(*args):
#             max_value = -1
#             max_position = None
#             for x in args:
#                 new_value = cycle_distance(k, i, x)
#                 if new_value > max_value:
#                     max_value = new_value
#                     max_position = x
#             return max_position
#
#         stack = []
#         for w in g.successors(v):
#             c = g.get_color(w)
#             if c!= PURPLE and  c != BLACK:
#                 stack.append(w)
#         inorder = []
#         while stack:
#             u = stack[-1]
#             c = g.get_color(u)
#             if c != ORANGE:
#                 g.set_color(u, ORANGE)
#                 g.property(u, "in", len(inorder))
#                 inorder.append(u)
#                 for w in g.successors(u):
#                     wc = g.get_color(w)
#                     if wc == PURPLE:
#                         new = revers[w]
#                         g.update_property(u, "min", cycle_min, new)
#                         g.update_property(u, "max", cycle_max, new)
#                     elif wc == ORANGE:
#                         g.update_property(u, "link", min, g.property(w, "in"))
#                     elif wc != BLACK and wc != RED:
#                         stack.append(w)
#             else:
#                 g.set_color(u, RED)
#                 stack.pop()
#                 for w in g.successors(u):
#                     wc = g.get_color(w)
#                     if wc != PURPLE and wc != BLACK:
#                         g.update_property(u, "min", cycle_min, g.property(w, "min"), g.property(w, "max"))
#                         g.update_property(u, "max", cycle_max, g.property(w, "min"), g.property(w, "max"))
#                         g.update_property(u, "link", min, g.property(w, "link"))
#         for w in inorder:
#             if g.property(w, "link") and g.property(w, "link") != inf:
#                 other = inorder[int(g.property(w, "link"))]
#                 g.update_property(w, "min", cycle_min, g.property(other, "min"))
#                 g.update_property(w, "max", cycle_max, g.property(other, "max"))
#                 g.property(w, "link", inf)
#         maxlist = []
#         for w in g.successors(v):
#             c = g.get_color(w)
#             if c != PURPLE:
#                 maxlist.append(g.property(w, "min"))
#                 maxlist.append(g.property(w, "max"))
#             elif c != BLACK:
#                 maxlist.append(revers[w])
#         maxlist = filter(lambda x: x is not None, maxlist)
#
#         ret.append(cycle_max(*maxlist))
#     return ret


# def max_distance(paths, k, l, pos):
#     end = paths[pos]
#     max_dis = (0, None)
#     for i in l:
#         dis = cycle_distance(k, i, paths[i]) - cycle_distance(k, i, end)
#         if dis > max_dis[0]:
#             max_dis = (dis, i)
#     return max_dis


def generate_cycle_range(k, pos, end):
    i = pos
    if end < pos:
        while i < end or i >= pos:
            yield i
            i = (i + 1) % k
    else:
        while i < end:
            yield i
            i += 1


def find_cover_cut(cmax):
    k = len(cmax)
    #Calculate maximal global C-Path
    m = max((cycle_distance(k, i, cmax[i]), i) for i in range(k))[1]
    md = cycle_distance(k, m, cmax[m])
    laststart = m
    lastend = m
    #While laststart end not in maximal global C-Path
    while  md <= cycle_distance(k, m, cmax[laststart]):
        #Calc maximal overtower
        next = None
        max_dist = 0
        for i in generate_cycle_range(k, lastend, cmax[laststart]):
            #Filter included paths
            if cycle_distance(k, i, cmax[i]) <= cycle_distance(k, i, cmax[laststart]):
                continue
            #Calc overtower and save max
            if cycle_distance(k, cmax[laststart], cmax[i]) > max_dist:
                max_dist = cycle_distance(k, cmax[laststart], cmax[i])
                next = i
        #If nothing overtower
        if next is None:
            #Return cut point
            return True, cmax[laststart]
        #Set next path to check
        lastend = cmax[laststart]
        laststart = next
    #Return Cycle cover
    return False, cmax[laststart]
    
    # if m[0] == k:
    #     return m[1]
    # j = m[1]
    #
    # outset = set(generate_cycle_range(k, j, paths[j]))
    # outset.add(paths[j])
    # while True:
    #     n = max_distance(paths, k, generate_cycle_range(k, j, paths[j]), j)
    #     if n[0] == 0:
    #         return paths[j]
    #     j = n[1]
    #     if paths[j] in outset:
    #         return m[1]


def create_dfs_order(v, g, cycle):
    order = Order()
    stack = [v]
    v2 = None
    while stack:
        u = stack[-1]
        c = g.get_color(u)
        if c != GREY and c != BLACK:
            g.set_color(u, GREY)
            for w in g.successors(u):
                if cycle and w == v:
                    v2 = "{v}_split_duplicate".format(v=v)
                    order.add(v2)
                    cycle = False
                color = g.get_color(w)
                if color != GREY and color != BLACK:
                    stack.append(w)
        else:
            stack.pop()
            if c == GREY:
                order.add(u)
                g.set_color(u, BLACK)
    return order, v2
    

class Order:
    """A order representation.
    Get a vertex on an arbitrary position in O(1).
    Get the position of an arbitrary vertex in O(1)."""
    
    def __init__(self):
        """Init the order set source position -1 and sink and None position to infinity """
        self.order = []
        self.revers_order = {None: inf}
        self.pos = 0
    
    def add(self, v):
        """Add an element to the end of the order"""
        self.order.append(v)
        self.revers_order[v] = self.pos
        self.pos += 1
    
    def __len__(self):
        return len(self.order)
    
    def revers(self):
        self.order = list(reversed(self.order))
        for i in range(len(self.order)):
            self.revers_order[self.order[i]] = i
    
    @property
    def n(self):
        """Get the length of the order."""
        return len(self.order)
    
    def __getitem__(self, item):
        """Get element at position item"""
        return self.order[item]
    
    def get_position(self, v):
        """Get position of element v. If v not contained return -2"""
        try:
            return self.revers_order[v]
        except KeyError:
            return -2
        
    def __contains__(self, item):
        return item in self.revers_order
        
    def __str__(self):
        return str(self.order)


def out_parent(k, g, order, v, v2):
    u = order[k]
    if u == v2:
        u = v
    if g.in_degree(u) == 0:
        return inf
    maximum = -1
    for w in g.predecessors(u):
        pos = order.get_position(w)
        if pos <= k:
            return inf
        maximum = max(maximum, pos)
    return maximum


def out_child(k, g, order, v, v2):
    u = order[k]
    if u == v2:
        u = v
    if g.out_degree(u) == 0:
        return -2
    minimum = inf
    for w in g.successors(u):
        if w == v and v2 is not None:
            pos = order.get_position(v2)
        else:
            pos = order.get_position(w)
        if pos >= k:
            return -2
        minimum = min(minimum, pos)
    return minimum


def superbubble(g, order, reporter, v, v2):
    """Detect all superbubbles in a DAG."""
    
    def report(i, o):
        reporter.rep(order[o: i + 1][::-1])
    
    stack = []
    out_parent_map = []
    t = None
    for k in range(len(order)):
        child = out_child(k, g, order, v, v2)
        if child == k - 1:
            stack.append(t)
            t = k - 1
        else:
            while t is not None and t > child:
                t2 = stack.pop()
                if t2 is not None:
                    out_parent_map[t2] = max(out_parent_map[t], out_parent_map[t2])
                t = t2
        if t is not None and out_parent_map[t] == k:
            report(k, t)
            t2 = stack.pop()
            if t2 is not None:
                out_parent_map[t2] = max(out_parent_map[t], out_parent_map[t2])
            t = t2
        out_parent_map.append(out_parent(k, g, order, v, v2))
        if t is not None:
            out_parent_map[t] = max(out_parent_map[t], out_parent_map[k])


class SCCFilter(Filter):
    """The filter that correct the artifical vertex and discards false added superbubble."""
    def __init__(self, reporter, v, v2):
        super().__init__(reporter)
        self.v = v
        self.v2 = v2
    
    def rep(self, dag,):
        if dag[-1] == self.v2:
            dag[-1] = self.v
        if dag[0] != dag[-1]:
            self.report(dag)


class ColordGraph:
    """The auxiliary graph representation.
    It is in the core a subgraph of the complete NetworkX graph.
    However, it have an other initialisation, some extra features and depend slightly different."""
    
    def __init__(self, g):
        """Save the the graph."""
        self.g = g
    
    def in_degree(self, v):
        """Get the in degree of a vertex."""
        return self.g.in_degree(v)
    
    def out_degree(self, v):
        """Get the out degree of a vertex"""
        return self.g.out_degree(v)
    
    def successors(self, v):
        """Get all successors of a vertex."""
        return list(self.g.successors(v))
    
    def predecessors(self, v):
        """Get all predeccessors of a vertex."""
        return list(self.g.predecessors(v))
    
    @property
    def nodes(self):
        """Get all vertices of a graph (including a and b)."""
        return self.g.nodes
    
    def set_color(self, v, c):
        """Set the color of v to c."""
        self.g.node[v]['c'] = c
    
    def get_color(self, v):
        """Get the color of v."""
        
        return self.g.node[v]['c']
    
    def property(self, v, key, value=None):
        if value is not None:
            self.g.node[v][key] = value
        else:
            try:
                return self.g.node[v][key]
            except KeyError:
                return None
        
    def update_property(self, v, key, func, *values):
        values = list(filter(lambda x: x is not None, values))
        if values:
            node = self.g.node[v]
            if key in node:
                node[key] = func(node[key], *values)
            else:
                if len(values) > 1:
                    node[key] = func(*values)
                else:
                    node[key] = values[0]
    
    def __iter__(self):
        """Iterate over the vertices of the graph (excluding a and b)."""
        return iter(self.nodes)
    
    def __str__(self):
        s = ", ".join("{v} {color}".format(v=v, color=self.get_color(v)) for v in self.nodes)
        s += "\n"
        s += ", ".join(str(s) for s in self.g.edges)
        s += "\n"
        return s


class hashed_list:
    def __init__(self, iteratable = None):
        self.list = []
        self.dict = {}
        if iteratable is not None:
            for v in iteratable:
                self.append(v)
        
        
    def append(self, v):
        self.dict[v] = len(self.list)
        self.list.append(v)
    
    def index(self, v):
        return self.dict[v]
    
    def __len__(self):
        return len(self.list)
    
    def __getitem__(self, item):
        return self.list[item]
    
    def __iter__(self):
        return iter(self.list)
    
    def __contains__(self, item):
        return item in self.dict
    
    def __str__(self):
        return str(self.list)
