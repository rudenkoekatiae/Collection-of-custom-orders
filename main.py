"""
main module
"""
from algorithm import cnf_file, cnf_inputs, solve_2sat, apply_request_to_cnf

def read_components_from_file(filename: str):
    """
    Docstring for read_components_from_file
    
    :param filename: Description
    :type filename: str
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None, None, None

    components = []
    for line in lines:
        if "REQUIRES" in line or "CONFLICTS" in line:
            break
        components.append(line)

    cnf_dict = cnf_file(filename)
    mapping = {comp: chr(97 + i) for i, comp in enumerate(components)}
    return cnf_dict, components, mapping

def manual_input_mode():
    """
    Docstring for manual_input_mode
    """
    print("Manual input mode\n")
    n = int(input("How many components? → "))
    components = [input("Component name: ").strip() for _ in range(n)]

    print("Enter REQUIRES rules (A B). Empty line to finish:")
    requirements = []
    while True:
        line = input("> ").strip()
        if not line:
            break
        parts = [p.strip().strip(",") for p in line.split()]
        if len(parts) != 2:
            print("Invalid format! Use: A B")
            continue
        a, b = parts
        if a not in components or b not in components:
            print("Unknown component in rule.")
            continue
        requirements.append((a, b))

    print("Enter CONFLICTS rules (A B). Empty line to finish:")
    conflicts = []
    while True:
        line = input("> ").strip()
        if not line:
            break
        parts = [p.strip().strip(",") for p in line.split()]
        if len(parts) != 2:
            print("Invalid format! Use: A B")
            continue
        a, b = parts
        if a not in components or b not in components:
            print("Unknown component in rule.")
            continue
        conflicts.append((a, b))

    cnf_dict, mapping = cnf_inputs(requirements, conflicts, components)
    return cnf_dict, components, mapping

def get_customer_request(components):
    """
    Docstring for get_customer_request
    
    :param components: Description
    """
    print("Customer configuration")
    print("Available components:", ", ".join(components))
    raw = input("Enter desired components (comma or space separated): ").strip()
    parts = [p.strip().strip(",") for p in raw.replace(",", " ").split()]
    invalid = [p for p in parts if p not in components]
    if invalid:
        print("Invalid components:", ", ".join(invalid))
        return None
    return parts

def main():
    """
    Docstring for main
    """
    print("Equipment Configuration Solver (2-SAT)\n")
    print("1 — load configuration from file")
    print("2 — enter configuration manually")

    choice = input("Your choice: ").strip()

    if choice == "1":
        filename = input("Enter filename: ").strip()
        cnf_dict, components, mapping = read_components_from_file(filename)
        if cnf_dict is None:
            return
    elif choice == "2":
        cnf_dict, components, mapping = manual_input_mode()
    else:
        print("Invalid choice.")
        return

    request = get_customer_request(components)
    if request is None:
        return

    full_cnf = apply_request_to_cnf(cnf_dict, request, mapping)
    assignment = solve_2sat(full_cnf)

    print("Result")
    if assignment is None:
        print("Configuration is NOT possible due to conflicting rules.\n")
        print("Check the following:")
        print("  - REQUIRES rules that cannot be satisfied")
        print("  - CONFLICTS rules violated by your selection")
    else:
        print("Configuration is possible!")
        print("Enabled components (including required by REQUIRES):")
        for comp, var in mapping.items():
            if assignment.get(var, False):
                mark = "(requested)" if comp in request else "(required)"
                print(f"  - {comp} {mark}")

if __name__ == "__main__":
    main()
