"""The package that constructs the dags out of the SCC that is also a CC."""
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


def cycledecompose(c):
    cycle = find_cycle(c)
    paths = find_paths(c, cycle)
    cut = cycle[find_cover_cut(paths)]
    alt = split_cycle(c, cut)
    return cut, alt


def find_cycle(c):
    r = next(iter(c))
    c.set_color(r, GREY, "f")
    stack = [(r, iter(c.successors(r)))]
    while stack:
        parent, children = stack[-1]
        try:
            child = next(children)
            if c.has_no_color(child, "f"):
                c.set_color(child, GREY, "f")
                stack.append((child, iter(c.successors(child))))
            elif c.get_color(child, "f") == GREY:
                ret = []
                for v in stack:
                    if len(ret) != 0 or v[0] == child:
                        ret.append(v[0])
                return ret
        except StopIteration:
            stack.pop()


def find_paths(c, cycle):
    revers = {}
    for i in range(len(cycle)):
        c.set_color(cycle[i], WHITE, "c")
        revers[cycle[i]] = i
        
    values = {}
    k = len(cycle)
    for v in c.nodes:
        values[v] = [None, None, inf]
    
    for i in range(len(cycle)):
        def newmin(*args):
            try:
                return min(map(lambda x: ((x - i-1) % k, x), filter(lambda x: x is not None, args)))[1]
            except ValueError:
                return None
        
        def newmax(*args):
            try:
                return max(map(lambda x: ((x - i-1) % k, x), filter(lambda x: x is not None, args)))[1]
            except ValueError:
                return None
        r = cycle[i]
        stack = [(r, iter(c.successors(r)))]
        inorder = []
        revin = {}
        while stack:
            parent, children = stack[-1]
            try:
                child = next(children)
                if c.has_no_color(child, "c"):
                    c.set_color(child, GREY, "c")
                    revin[child] = len(inorder)
                    inorder.append(child)
                    stack.append((child, iter(c.successors(child))))
                elif c.get_color(child, "c") == WHITE:
                    new = revers[child]
                    value = values[parent]
                    value[0] = newmin(value[0], new)
                    value[1] = newmax(value[1], new)
                elif c.get_color(child, "c") == GREY:
                    value = values[parent]
                    value[2] = min(value[2], revin[child])
            except StopIteration:
                value = values[parent]
                for sucs in c.successors(parent):
                    if c.get_color(sucs, "c") != WHITE:
                        value_suc = values[sucs]
                        value[0] = newmin(value[0], value_suc[0], value_suc[1])
                        value[1] = newmax(value[1], value_suc[1], value_suc[0])
                        value[2] = min(value[2], value_suc[2])
                if c.get_color(parent, "c") == GREY:
                    c.set_color(parent, BLACK, "c")
                stack.pop()
        for v in inorder:
            if values[v][2] != inf:
                other = inorder[values[v][2]]
                values[v][0] = newmin(values[v][0], values[other][0])
                values[v][1] = newmax(values[v][1], values[other][1])
                values[v][2] = inf
 
    return [values[v][1] for v in cycle]


def find_cover_cut(paths):
    k = len(paths)
    
    def distance(i, end):
        if end > i:
            return end-i
        return end+k-i
    
    def get_max(l, pos):
        end = paths[pos]
        return max((distance(i, paths[i]) - distance(i, end), i) for i in l)

    def generate_cycle_range(pos):
        end = paths[pos]
        i = pos
        if end < pos:
            while i < end or i >= pos:
                yield i
                i = (i+1) % k
        else:
            while i < end:
                yield i
                i += 1

    m = max((distance(i, paths[i]), i) for i in range(k))
    if m[0] == k:
        return m[1]
    j = m[1]
    
    outset = set(generate_cycle_range(j))
    outset.add(paths[j])
    while True:
        n = get_max(generate_cycle_range(j), j)
        if n[0] == 0:
            return paths[j]
        j = n[1]
        if paths[j] in outset:
            return m[1]


def split_cycle(c, v):
    alt_v = "{v}_2".format(v=v)
    for pre in c.predecessors(v):
        c.add_edge(pre, alt_v)
        c.remove_edge(pre, v)
    c.connect2source(v)
    c.connect2sink(alt_v)
    return alt_v

# Order creatrion


def toposort2(g):
    """Do a topological ordering of the graph.
    It does a linear version of a deep first search.
    """
    v = next(iter(g.nodes))
    order = Order()
    stack = [(v, iter(g.successors(v)))]
    while stack:
        parent, children = stack[-1]
        try:
            child = next(children)
            if g.has_no_color(child):
                stack.append((child, iter(g.successors(child))))
                g.set_color(child, GREY)
        except StopIteration:
            stack.pop()
            order.add(parent)
            g.set_color(parent, BLACK)
    return order


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


# Detecter stuff

def out_parent2(k, g, order):
    v = order[k]
    if g.in_degree(v) == 0:
        return inf
    maximum = -1
    for v2 in g.predecessors(v):
        pos = order.get_position(v2)
        if pos < k or v2 == g.a:
            return inf
        maximum = max(maximum, pos)
    return maximum


def out_child2(k, g, order):
    v = order[k]
    if g.out_degree(v) == 0:
        return -2
    minimum = inf
    for v2 in g.successors(v):
        pos = order.get_position(v2)
        if pos > k or v2 == g.b:
            return -2
        minimum = min(minimum, pos)
    return minimum


def dag_superbubble2(g, order, reporter):
    """Detect all superbubbles in a DAG."""
    
    def report(i, o):
        reporter.rep(order[o: i + 1][::-1])
    
    stack = []
    out_parent_map = []
    t = None
    for k in range(len(order)):
        child = out_child2(k, g, order)
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
        out_parent_map.append(out_parent2(k, g, order))
        if t is not None:
            out_parent_map[t] = max(out_parent_map[t], out_parent_map[k])

# Filter


class SCCFilter(Filter):
    """The filter that correct the artifical vertex and discards false added superbubble."""
    def __init__(self, reporter, v, alt):
        super().__init__(reporter)
        self.v = v
        self.alt = alt

    def rep(self, dag):
        if dag[-1] == self.alt:
            if dag[0] == self.v:
                return
            dag[-1] = self.v
        self.report(dag)
