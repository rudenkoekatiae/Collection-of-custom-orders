"""
Генератор конфігурацій продукту для 2-SAT задачі.
Поточні шаблони: кавовий_апарат.
Підтримка додавання нових шаблонів у майбутньому.
"""

TEMPLATES = {
    "кавовий_апарат": {
        "product": "КавовийАпарат_Стандарт",
        "components": [
            "РезервуарМолока",
            "Тент",
            "КаналПромивки",
            "ВеликийРезервуарВоди",
            "ДодатковийТен",
        ],
        "dependencies": [
            "РезервуарМолока REQUIRES Тент",
            "РезервуарМолока REQUIRES КаналПромивки",
            "ТенМолока REQUIRES КаналПромивки",
            "ВеликийРезервуарВоди CONFLICTS ДодатковийТен",
        ]
    }
}


def create_config_file(template_name, filename="config.txt"):
    """Створює файл конфігурації на основі шаблону"""

    if template_name not in TEMPLATES:
        print(f"Шаблон '{template_name}' не знайдено!")
        print(f"Доступні шаблони: {', '.join(TEMPLATES.keys())}")
        return False

    data = TEMPLATES[template_name]

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"{data['product']}\n")
        f.write(f"{len(data['components'])}\n")
        for comp in data['components']:
            f.write(f"{comp}\n")
        f.write(f"{len(data['dependencies'])}\n")
        for dep in data['dependencies']:
            f.write(f"{dep}\n")

    print(f"Файл '{filename}' успішно створено!\n ")
    return True


def create_custom_config():
    """Інтерактивне створення власної конфігурації"""

    product = input("Назва базового продукту: ")

    print("Додавання компонент\n")
    print("(введіть порожній рядок для завершення)\n")
    components = []
    while True:
        comp = input(f"Компонента {len(components)+1}: ")
        if not comp:
            break
        components.append(comp)

    if not components:
        print("Потрібно додати хоча б одну компоненту!\n")
        return

    print("Додавання залежностей\n")
    print("Формат: A REQUIRES B або A CONFLICTS B\n")
    dependencies = []
    while True:
        dep = input(f"Залежність {len(dependencies)+1}: ")
        if not dep:
            break
        if "REQUIRES" not in dep and "CONFLICTS" not in dep:
            print("Залежність має містити REQUIRES або CONFLICTS\n")
            continue
        dependencies.append(dep)

    filename = input("Ім'я файлу (config.txt): \n") or "config.txt"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"{product}\n")
        f.write(f"{len(components)}\n")
        for comp in components:
            f.write(f"{comp}\n")
        f.write(f"{len(dependencies)}\n")
        for dep in dependencies:
            f.write(f"{dep}\n")

    print(f"Файл '{filename}' успішно створено!\n")


def show_templates():
    """
    показує доступні шаблони
    """
    print("Доступні шаблони:\n")
    for i, name in enumerate(TEMPLATES.keys(), 1):
        print(f"{i}. {name}")


if __name__ == "__main__":

    print("Оберіть дію:")
    print("1 - Створити конфігурацію з шаблону")
    print("2 - Створити власну конфігурацію")

    choice = input("Ваш вибір (1-2): \n")

    if choice == "1":
        show_templates()
        template_choice = input("Введіть назву шаблону: \n")
        filename = input("Ім'я файлу (config.txt): ") or "config.txt"
        create_config_file(template_choice, filename)

    elif choice == "2":
        create_custom_config()

    else:
        print("Вибір недоступний\n")


    print("Готово!\n")
