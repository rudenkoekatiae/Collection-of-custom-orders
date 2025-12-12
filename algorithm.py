"""
Algorithm module for Equipment Configuration Solver (2-SAT)
- cnf_file()      → parse config file to CNF
- cnf_inputs()    → parse manual input to CNF
- apply_request_to_cnf() → add customer requests to CNF
- build_graph_from_cnf() → implication graph
- tarjan()        → strongly connected components
- solve_2sat()    → check satisfiability and produce assignment
"""

def cnf_file(input_file: str) -> dict[str, list[str]]:
    """
    Docstring for cnf_file
    
    :param input_file: Description
    :type input_file: str
    :return: Description
    :rtype: dict[str, list[str]]
    """
    components = []
    rules = []

    with open(input_file, "r", encoding="utf-8") as f:
        raw_lines = [line.strip() for line in f if line.strip()]

    reading_rules = False
    for line in raw_lines:
        if "REQUIRES" in line or "CONFLICTS" in line:
            reading_rules = True

        if not reading_rules:
            components.append(line)
        else:
            rules.append(line)

    appropriation = {comp: chr(97 + i) for i, comp in enumerate(components)}
    cnf = {}

    def add_rule(a, b):
        cnf.setdefault(a, []).append(b)

    for rule in rules:
        if "REQUIRES" in rule:
            left, right = [p.strip() for p in rule.split("REQUIRES")]
            add_rule(appropriation[left], appropriation[right])
        elif "CONFLICTS" in rule:
            left, right = [p.strip() for p in rule.split("CONFLICTS")]
            a, b = appropriation[left], appropriation[right]
            add_rule(a, f"not {b}")
            add_rule(b, f"not {a}")

    return cnf

def cnf_inputs(requirements, conflicts, components):
    """
    Docstring for cnf_inputs
    
    :param requirements: Description
    :param conflicts: Description
    :param components: Description
    """
    cnf = {}
    appropriation = {comp: chr(97 + i) for i, comp in enumerate(components)}

    def add(a, b):
        cnf.setdefault(a, []).append(b)

    for a, b in requirements:
        add(appropriation[a], appropriation[b])

    for a, b in conflicts:
        x = appropriation[a]
        y = appropriation[b]
        add(x, f"not {y}")
        add(y, f"not {x}")

    return cnf, appropriation
def apply_request_to_cnf(cnf_dict, request, mapping):
    """
    Force requested components to True.
    Implemented as adding clause: not X -> X
    """
    cnf = {k: v.copy() for k, v in cnf_dict.items()}
    for comp in request:
        var = mapping[comp]
        cnf.setdefault(f"not {var}", []).append(var)
    return cnf

def build_graph_from_cnf(cnf):
    """
    Each clause A -> B is added as edge A->B and not B -> not A
    """
    graph = {}
    for a, implies in cnf.items():
        for b in implies:
            graph.setdefault(a, []).append(b)

            na = a[4:] if a.startswith("not ") else a
            nb = b[4:] if b.startswith("not ") else b
            not_a = "not " + na
            not_b = "not " + nb
            graph.setdefault(not_b, []).append(not_a)

    return graph

def tarjan(graph):
    """
    Docstring for tarjan
    
    :param graph: Description
    """
    index = [0]
    stack = []
    onstack = set()
    indices = {}
    lowlink = {}
    result = []

    def dfs(v):
        indices[v] = index[0]
        lowlink[v] = index[0]
        index[0] += 1
        stack.append(v)
        onstack.add(v)

        for w in graph.get(v, []):
            if w not in indices:
                dfs(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in onstack:
                lowlink[v] = min(lowlink[v], indices[w])

        if lowlink[v] == indices[v]:
            comp = []
            while True:
                w = stack.pop()
                onstack.remove(w)
                comp.append(w)
                if w == v:
                    break
            result.append(comp)

    for v in graph:
        if v not in indices:
            dfs(v)

    return result
def solve_2sat(cnf_dict):
    """
    Docstring for solve_2sat
    
    :param cnf_dict: Description
    """
    graph = build_graph_from_cnf(cnf_dict)
    scc = tarjan(graph)

    comp_index = {}
    for i, comp in enumerate(scc):
        for v in comp:
            comp_index[v] = i

    variables = set()
    for v in comp_index:
        if not v.startswith("not "):
            nv = "not " + v
            if nv in comp_index and comp_index[nv] == comp_index[v]:
                return None
            variables.add(v)

    order = sorted(variables, key=lambda x: comp_index[x], reverse=True)
    assignment = {}
    for v in order:
        if v not in assignment:
            assignment[v] = True
            assignment["not " + v] = False

    return assignment
