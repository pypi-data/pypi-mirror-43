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
PURPLE = 5
"""COLOR Definition Part of a cycle"""
ORANGE = 6
"""COLOR Definition Seen in a path search"""
RED = 7
"""COLOR Definition Seen in a path search"""


def abitarry_graph_detect(graph, rep):
    g = ColordGraph(graph)
    for v in g.nodes:
        g.set_color(v, WHITE)
    for v, alt in generate_starts(g):
        order, pos = create_dfs_order(v, g, alt)
        superbubble(g, order, SCCFilter(rep), alt, pos)


def generate_starts(g):
    for v in g.nodes:
        if g.in_degree(v) == 0:
            yield v, None
    
    for cycle in find_cycles2(g):
        paths = find_paths2(g, cycle)
        cut = cycle[find_cover_cut(paths)]
        yield cut, cut


def find_cycles(g):
    for v in g.nodes:
        if g.get_color(v) == WHITE:
            g.set_color(v, GREEN)
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
                            cycle = [stack.pop()]
                            g.set_color(w, PURPLE)
                            while stack[-1] != w:
                                x = stack.pop()
                                if g.get_color(x) == GREEN:
                                    g.set_color(x, PURPLE)
                                    cycle.append(x)
                            yield list(reversed(cycle))
                            break
                elif c == GREEN:
                    g.set_color(u, YELLOW)
                    stack.pop()


def find_cycles2(g):
    for v in g.nodes:
        if g.get_color(v) == WHITE:
            g.set_color(v, GREEN)
            stack = [(v, iter(g.successors(v)))]
            while stack:
                parent, children = stack[-1]
                if g.get_color(parent) == BLACK:
                    stack.pop()
                else:
                    try:
                        child = next(children)
                        color = g.get_color(child)
                        if color == WHITE:
                            g.set_color(child, GREEN)
                            stack.append((child, iter(g.successors(child))))
                        elif color == GREEN:
                            k = 0
                            for k in range(len(stack)):
                                if stack[k][0] == child:
                                    break
                            yield [x[0] for x in stack[k:]]
                            stack = stack[:k]
                    except StopIteration:
                        g.set_color(parent, YELLOW)
                        stack.pop()


def cycle_distance(k, i, end):
    if end > i:
        return end - i - 1
    return end + k - i - 1


def find_paths(g, cycle):
    revers = {}
    for i in range(len(cycle)):
        revers[cycle[i]] = i
    k = len(cycle)
    
    def cycle_min(*args):
        min_value = inf
        ret = None
        for x in args:
            new_value = cycle_distance(k, i, x)
            if new_value < min_value:
                min_value = new_value
                ret = x
        return ret
    
    def cycle_max(*args):
        max_value = -1
        ret = None
        for x in args:
            new_value = cycle_distance(k, i, x)
            if new_value > max_value:
                max_value = new_value
                ret = x
        return ret
    
    ret = []
    
    for v in cycle:
        stack = []
        for w in g.successors(v):
            if g.get_color(w) != PURPLE:
                stack.append(w)
        
        inorder = []
        while stack:
            u = stack[-1]
            c = g.get_color(u)
            if c != ORANGE:
                g.set_color(u, ORANGE)
                g.property(u, "in", len(inorder))
                inorder.append(u)
                for w in g.successors(u):
                    wc = g.get_color(w)
                    if wc == PURPLE:
                        new = revers[w]
                        g.update_property(u, "min", cycle_min, new)
                        g.update_property(u, "max", cycle_max, new)
                    elif wc == ORANGE:
                        g.update_property(u, "link", min, g.property(w, "in"))
                    elif wc != BLACK and wc != RED:
                        stack.append(w)
            else:
                g.set_color(u, RED)
                stack.pop()
                for w in g.successors(u):
                    g.update_property(u, "min", cycle_min, g.property(w, "min"), g.property(w, "max"))
                    g.update_property(u, "max", cycle_max, g.property(w, "min"), g.property(w, "max"))
                    g.update_property(u, "link", min, g.property(w, "link"))
        for w in inorder:
            if g.property(w, "link"):
                other = inorder[g.property(w, "link")]
                g.update_property(w, "min", cycle_min, g.property(other, "min"))
                g.update_property(w, "max", cycle_max, g.property(other, "max"))
                g.property(w, "link", inf)
        maxlist = []
        for w in g.successors(v):
            if g.get_color(w) != PURPLE:
                maxlist.append(g.property(w, "min"))
                maxlist.append(g.property(w, "max"))
            else:
                maxlist.append(revers[w])
        ret.append(cycle_max(maxlist))
    return ret


def find_paths2(g, cycle):
    revers = {}
    for i in range(len(cycle)):
        revers[cycle[i]] = i
    k = len(cycle)

    def cycle_min(*args):
        min_value = inf
        ret = None
        for x in args:
            new_value = cycle_distance(k, i, x)
            if new_value < min_value:
                min_value = new_value
                ret = x
        return ret

    def cycle_max(*args):
        max_value = -1
        ret = None
        for x in args:
            new_value = cycle_distance(k, i, x)
            if new_value > max_value:
                max_value = new_value
                ret = x
        return ret
    
    for i in range(len(cycle)):
        r = cycle[i]
        stack = [(r, iter(g.successors(r)))]
        inorder = []
        while stack:
            parent, children = stack[-1]
            try:
                child = next(children)
                color = g.get_color(child)
                if color == PURPLE:
                    new = revers[child]
                    g.update_property(parent, "min", cycle_min, new)
                    g.update_property(parent, "max", cycle_max, new)
                elif color == ORANGE:
                    g.update_property(parent, "link", min, g.property(child, "in"))
                elif color != BLACK and color != RED:
                    g.set_color(child, ORANGE)
                    g.property(child, "in", len(inorder))
                    inorder.append(child)
                    stack.append((child, iter(g.successors(child))))
            except StopIteration:
                for suc in g.successors(parent):
                    color = g.get_color(suc)
                    if color != PURPLE and color != BLACK:
                        g.update_property(parent, "min", cycle_min, g.property(suc, "min"), g.property(suc, "max"))
                        g.update_property(parent, "max", cycle_max, g.property(suc, "min"), g.property(suc, "max"))
                        g.update_property(parent, "link", min, g.property(suc, "link"))
                if g.get_color(parent) == ORANGE:
                    g.set_color(parent, RED)
                stack.pop()
        for v in inorder:
            if g.property(v, "link"):
                other = inorder[g.property(v, "link")]
                g.update_property(v, "min", cycle_min, g.property(other, "min"))
                g.update_property(v, "max", cycle_max, g.property(other, "max"))
                g.property(v, "link", inf)
    
    return [g.property(v, "max") for v in cycle]


def max_distance(paths, k, l, pos):
    end = paths[pos]
    max_dis = (0, None)
    for i in l:
        dis = cycle_distance(k, i, paths[i]) - cycle_distance(k, i, end)
        if dis > max_dis[0]:
            max_dis = (dis, i)
    return max_dis


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


def find_cover_cut(paths):
    k = len(paths)
    m = max((cycle_distance(k, i, paths[i]), i) for i in range(k))
    if m[0] == k:
        return m[1]
    j = m[1]
    
    outset = set(generate_cycle_range(k, j, paths[j]))
    outset.add(paths[j])
    while True:
        n = max_distance(paths, k, generate_cycle_range(k, j, paths[j]), j)
        if n[0] == 0:
            return paths[j]
        j = n[1]
        if paths[j] in outset:
            return m[1]


def create_dfs_order(v, g, alt=None):
    """Do a topological ordering of the graph.
    It does a linear version of a deep first search.
    """
    order = Order()
    stack = [(v, iter(g.successors(v)))]
    g.set_color(v, GREY)
    first = alt is not None
    pos = None
    while stack:
        parent, children = stack[-1]
        try:
            child = next(children)
            if first and child == alt:
                first = False
                pos = order.pos
                order.add(child)
            color = g.get_color(child)
            if color != GREY and color != BLACK:
                stack.append((child, iter(g.successors(child))))
                g.set_color(child, GREY)
        except StopIteration:
            stack.pop()
            order.add(parent)
            g.set_color(parent, BLACK)
    return order, pos


class Order:
    """A order representation.
    Get a vertex on an arbitrary position in O(1).
    Get the position of an arbitrary vertex in O(1)."""
    
    def __init__(self):
        """Init the order set source position -1 and sink and None position to infinity """
        self.order = []
        self.revers = {None: inf}
        self.pos = 0
    
    def add(self, v):
        """Add an element to the end of the order"""
        self.order.append(v)
        self.revers[v] = self.pos
        self.pos += 1
    
    def __len__(self):
        return len(self.order)
    
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
            return self.revers[v]
        except KeyError:
            return -2


def out_parent3(k, g, order):
    v = order[k]
    if g.in_degree(v) == 0:
        return inf
    maximum = -1
    for v2 in g.predecessors(v):
        pos = order.get_position(v2)
        if pos <= k:
            return inf
        maximum = max(maximum, pos)
    return maximum


def out_child3(k, g, order, alt, altpos):
    v = order[k]
    if g.out_degree(v) == 0:
        return -2
    minimum = inf
    for v2 in g.successors(v):
        if v2 == alt:
            pos = altpos
        else:
            pos = order.get_position(v2)
        if pos >= k:
            return -2
        minimum = min(minimum, pos)
    return minimum


def superbubble(g, order, reporter, alt=None, pos=0):
    """Detect all superbubbles in a DAG."""
    
    def report(i, o):
        reporter.rep(order[o: i + 1][::-1])
    
    stack = []
    out_parent_map = []
    t = None
    for k in range(len(order)):
        child = out_child3(k, g, order, alt, pos)
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
        out_parent_map.append(out_parent3(k, g, order))
        if t is not None:
            out_parent_map[t] = max(out_parent_map[t], out_parent_map[k])


class SCCFilter(Filter):
    """The filter that correct the artifical vertex and discards false added superbubble."""
    
    def rep(self, dag):
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
