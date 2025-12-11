"""
Алгоритм 2-SAT для перевірки можливості конфігурації
"""

def read_config_from_file(file_content):
    """
    Читає конфігурацію продукту з файлу.

    Формат файлу:
    - Кожен рядок містить або назву компонента, або правило
    - Правила: A REQUIRES B або A CONFLICTS B
    - Порожні рядки та рядки з # пропускаються

    Args:
        file_content: bytes або str - вміст файлу

    Returns:
        dict: інформація про продукт або None при помилці
    """
    try:
        if isinstance(file_content, bytes):
            content = file_content.decode('utf-8')
        else:
            content = file_content

        lines = content.split('\n')

        # Структура для зберігання даних
        all_components = set()
        requirements = []
        conflicts = []

        # Обробка рядків
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if 'REQUIRES' in line:
                parts = line.split('REQUIRES')
                if len(parts) == 2:
                    a = parts[0].strip()
                    b = parts[1].strip()
                    requirements.append((a, b))
                    all_components.add(a)
                    all_components.add(b)
            elif 'CONFLICTS' in line:
                parts = line.split('CONFLICTS')
                if len(parts) == 2:
                    a = parts[0].strip()
                    b = parts[1].strip()
                    conflicts.append((a, b))
                    all_components.add(a)
                    all_components.add(b)
            else:
                # Просто назва компонента
                all_components.add(line)

        # Створюємо об'єкт продукту
        product_info = {
            'name': 'Кастомний продукт',
            'icon': '📄',
            'components': sorted(list(all_components)),
            'requirements': requirements,
            'conflicts': conflicts,
            'description': 'Продукт завантажений з файлу конфігурації',
            'component_descriptions': {}
        }

        return product_info

    except Exception as e:
        raise Exception(f"Помилка читання файлу: {str(e)}")

def cnf_inputs(requirements, conflicts, all_components)-> dict[str, str]:
    """
    Reads rules from user inputs and converts them to conjunctive normal form (CNF).

    Conversion logic:
    - ‘A REQUIRES B’ (A -> B) is converted to ‘{'A': ['B']}’.
    - ‘A CONFLICTS B’ (A xor B) is converted to ‘{'A': ['not B']}’.

    Returns:
        dict: Dictionary containing constraint rules grouped by variables
    """
    result_cnf = {}
    appropriation = {}
    for idx, comp in enumerate(all_components):
        appropriation[comp] = chr(97 + idx)

    for a, b in requirements:
        key = appropriation[a]
        value = appropriation[b]

        if key in result_cnf:
            result_cnf[key].append(value)
        else:
            result_cnf.setdefault(key, [value])

    for a, b in conflicts:
        key_a = appropriation[a]
        key_b = appropriation[b]

        if key_a in result_cnf:
            result_cnf[key_a].append(f'not {key_b}')
        else:
            result_cnf.setdefault(key_a, [f'not {key_b}'])

        if key_b in result_cnf:
            result_cnf[key_b].append(f'not {key_a}')
        else:
            result_cnf.setdefault(key_b, [f'not {key_a}'])

    return result_cnf, appropriation


def build_graph_from_cnf(cnf_dict):
    """Побудова графа імплікацій з CNF"""
    graph = {}

    def add_edge(u, v):
        """Додає ребро у граф"""
        if u not in graph:
            graph[u] = []
        if v not in graph[u]:
            graph[u].append(v)

    for x, lst in cnf_dict.items():
        for y in lst:
            if y.startswith("not "):
                y2 = y[4:]
                # x → ¬y2
                add_edge(x, f"not {y2}")
                # y2 → ¬x
                add_edge(y2, f"not {x}")
            else:
                # x → y
                add_edge(x, y)
                # ¬y → ¬x
                add_edge(f"not {y}", f"not {x}")

    return graph


def tarjan_scc(graph):
    """Алгоритм Тар'яна для знаходження компонент сильної зв'язності"""
    stack = []
    indices = {}
    low = {}
    onstack = set()
    result = []
    index = [0]

    def dfs(v):
        indices[v] = index[0]
        low[v] = index[0]
        stack.append(v)
        onstack.add(v)
        index[0] += 1

        for w in graph.get(v, []):
            if w not in indices:
                dfs(w)
                low[v] = min(low[v], low[w])
            elif w in onstack:
                low[v] = min(low[v], indices[w])

        if low[v] == indices[v]:
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


def solve_2sat_from_rules(requirements, conflicts, all_components):
    """
    Основна функція для розв'язання 2-SAT на основі правил

    Args:
        requirements: список пар (A, B) де A REQUIRES B
        conflicts: список пар (A, B) де A CONFLICTS B
        all_components: список всіх доступних компонентів

    Returns:
        tuple: (можливість, призначення, повідомлення)
    """
    try:
        # Конвертуємо правила у CNF
        cnf_dict, appropriation = cnf_inputs(requirements, conflicts, all_components)

        # Будуємо граф імплікацій
        graph = build_graph_from_cnf(cnf_dict)

        # Знаходимо компоненти сильної зв'язності
        scc = tarjan_scc(graph)

        # Створюємо відображення вершина -> номер компоненти
        comp_index = {}
        for i, comp in enumerate(scc):
            for v in comp:
                comp_index[v] = i

        # Перевіряємо на наявність суперечностей (x та ¬x в одній компоненті)
        variables = set()
        for v in comp_index:
            if v.startswith("not "):
                base_var = v[4:]
                if base_var in comp_index and comp_index[base_var] == comp_index[v]:
                    # Знайшли суперечність
                    rev_appropriation = {v: k for k, v in appropriation.items()}
                    base_name = rev_appropriation.get(base_var, base_var)
                    return False, {}, f"Конфігурація неможлива: суперечність для компонента '{base_name}'"
                variables.add(base_var)
            else:
                variables.add(v)

        # Якщо не знайдено суперечностей, будуємо призначення
        ordering = sorted(variables, key=lambda x: comp_index[x], reverse=True)
        assignment = {}

        for v in ordering:
            if v not in assignment:
                # Якщо компонента x в більшій SCC ніж ¬x, призначаємо True
                not_v = f"not {v}"
                if not_v in comp_index and comp_index.get(v, -1) > comp_index.get(not_v, -1):
                    assignment[v] = True
                else:
                    assignment[v] = True  # За замовчуванням призначаємо True

        # Перетворюємо призначення назад на назви компонентів
        component_assignment = {}
        rev_appropriation = {v: k for k, v in appropriation.items()}

        for var, value in assignment.items():
            if var in rev_appropriation:
                component_assignment[rev_appropriation[var]] = value

        return True, component_assignment, "Конфігурація можлива!"

    except Exception as e:
        return False, {}, f"Помилка при розв'язанні: {str(e)}"


def find_feasible_configurations(requirements, conflicts, all_components):
    """
    Знаходить всі можливі конфігурації (не оптимально для великих наборів)
    """
    feasible_configs = []
    n = len(all_components)


    for mask in range(1 << n):
        selected = []
        for i in range(n):
            if mask & (1 << i):
                selected.append(all_components[i])

        # check configuration
        possible, _, _ = solve_2sat_from_rules(requirements, conflicts, all_components)


        if possible:
            # check requirements
            valid = True
            for a, b in requirements:
                if a in selected and b not in selected:
                    valid = False
                    break

            # check confliscts
            if valid:
                for a, b in conflicts:
                    if a in selected and b in selected:
                        valid = False
                        break

            if valid:
                feasible_configs.append(selected)

    return feasible_configs
