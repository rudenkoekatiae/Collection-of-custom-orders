"""Main function"""
from algorithm import cnf_file, cnf_inputs, solve_2sat


def read_components_from_file(filename: str):
    """
    Reads components and rules from file.
    Returns CNF dictionary + list of components.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None, None, None

    components = []
    for i, line in enumerate(lines):
        if "REQUIRES" in line or "CONFLICTS" in line:
            break
        components.append(line)

    cnf_dict = cnf_file(filename)
    mapping = {comp: chr(97 + i) for i, comp in enumerate(components)}
    return cnf_dict, components, mapping



def manual_input_mode():
    print("Manual input mode\n")
    all_components = []

    n = int(input("How many components? → "))
    for _ in range(n):
        comp = input("Component name: ").strip()
        all_components.append(comp)

    print("Enter REQUIRES rules (A B). Empty line to finish:\n")
    requirements = []
    while True:
        line = input("> ").strip()
        if line == "":
            break
        a, b = line.split()
        requirements.append((a, b))

    print("Enter CONFLICTS rules (A B). Empty line to finish:\n")
    conflicts = []
    while True:
        line = input("> ").strip()
        if line == "":
            break
        a, b = line.split()
        conflicts.append((a, b))

    cnf_dict, mapping = cnf_inputs(requirements, conflicts, all_components)
    return cnf_dict, all_components, mapping

def get_customer_request(all_components):
    print("Customer configuration\n")
    print("Available components:", ", ".join(all_components))

    raw = input("Enter desired components: ").strip()
    parts = [p.strip().strip(",") for p in raw.replace(",", " ").split()]
    for p in parts:
        if p not in all_components:
            print(f" Component '{p}' does not exist.")
            return None

    return parts


def apply_request_to_cnf(cnf_dict, request, mapping):
    """
    Add "must be True" constraints for chosen components.
    """
    cnf = dict(cnf_dict)

    for comp in request:
        var = mapping[comp]
        if var not in cnf:
            cnf[var] = []

    return cnf


def main():
    print("Equipment Configuration Solver (2-SAT)")
    print("1 — load configuration from file")
    print("2 — enter configuration manually")

    mode = input("Your choice: ").strip()
    if mode == "1":
        filename = input("Enter filename: ").strip()
        cnf_dict, components, mapping = read_components_from_file(filename)

        if cnf_dict is None:
            return

    elif mode == "2":
        cnf_dict, components, mapping = manual_input_mode()

    else:
        print("Invalid choice.")
        return

    request = get_customer_request(components)
    if request is None:
        return
    full_cnf = apply_request_to_cnf(cnf_dict, request, mapping)

    assignment = solve_2sat(full_cnf)

    print("Result\n")
    if assignment is None:
        print("Configuration is NOT possible due to conflicting rules.")
    else:
        print("Configuration is possible!")
        print("Enabled components:")

        for comp, var in mapping.items():
            if assignment.get(var, False):
                print("  -", comp)


if __name__ == "__main__":
    main()
