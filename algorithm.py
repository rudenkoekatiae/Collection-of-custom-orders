""" algorims and reading of the inout file"""
def cnf(input_file)-> dict:
    """
    Reads rules from a file and converts them to conjunctive normal form (CNF).

    Conversion logic:
    - ‘A REQUIRES B’ (A -> B) is converted to ‘{'A': ['B']}’.
    - ‘A CONFLICTS B’ (A xor B) is converted to ‘{'A': ['not B']}’.

    Args:
        input_file (str): Path to the file (utf-8) containing the names of objects
                         and the rules for their interaction.

    Returns:
        dict: Dictionary containing constraint rules grouped by variables
    """
    appropriation = {}
    result_cnf = {}
    with open (input_file, 'r', encoding='utf-8') as f:
        for index, line in enumerate(f):
            key, value = None, None
            line = line.strip()
            if 'REQUIRES' in line:
                if len(line.split())<=2:
                    parts = line.replace(' REQUIRES', '')
                    key = appropriation[parts]
                    value = appropriation[parts]
                else:
                    parts = line.split(' REQUIRES ')
                    key = appropriation[parts[0]]
                    value = appropriation[parts[-1]]

            elif 'CONFLICTS' in line:
                parts = line.split(' CONFLICTS ')
                key = appropriation[parts[0]]
                value = f'not {appropriation[parts[-1]]}'
            else:
                appropriation.setdefault(line, chr(index+97))

            if key:
                if key in result_cnf:
                    result_cnf[key].append(value)
                else:
                    if value == '[]':
                        result_cnf.setdefault(key, key)
                    result_cnf.setdefault(key, [value])

    return result_cnf

def build_graph_from_cnf(cnf_dict):
    graph = {}
    def add(u,v):
        graph.setdefault(u,[]).append(v)
    for x, lst in cnf_dict.items():
        for y in lst:
            if y.startswith("not "):
                y2 = y[4:]
                add(x, "not "+y2)
                add(y2, "not "+x)
            else:
                add(x, y)
                add("not "+y, "not "+x)

    return graph

def tarjan(graph):
    stack = []
    indices = {}
    low = {}
    onstack=set()
    result=[]
    index = [0]

    def dfs(v):
        indices[v] = index[0]
        low[v] = index[0]
        stack.append(v)
        onstack.add(v)
        index[0] += 1
        for w in graph.get(v,[]):
            if w not in indices:
                dfs(w)
                low[v]=min(low[v], low[w])
            elif w in onstack:
                low[v]=min(low[v], indices[w])
        if low[v]==indices[v]:
            comp=[]
            while True:
                w = stack.pop()
                onstack.remove(w)
                comp.append(w)
                if w==v:
                    break
            result.append(comp)
    for v in graph:
        if v not in indices:
            dfs(v)
    return result

def solve_2sat(cnf_dict):
    graph = build_graph_from_cnf(cnf_dict)
    scc = tarjan(graph)
    comp_index={}
    for i,comp in enumerate(scc):
        for v in comp:
            comp_index[v] = i
    variables=set()
    for v in comp_index:
        if v.startswith("not "):
            continue
        nv="not "+v
        if nv in comp_index and comp_index[nv]==comp_index[v]:
            return None
        variables.add(v)
    ordering=sorted(variables, key=lambda x: comp_index[x], reverse=True)
    assignment={}
    for v in ordering:
        if v not in assignment:
            assignment[v]=True
            assignment["not "+v]=False

    return assignment


if __name__ == '__main__':
    print(f'{cnf('phone.txt')} for phone')
    print(f'{cnf('cofee.txt')} for coffee')
