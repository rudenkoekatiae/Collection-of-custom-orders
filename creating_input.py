"""
Генератор конфігурацій продукту для 2-SAT задачі.
Шаблони: кавовий_апарат, фехтувальна_екіпіровка, пилосос
"""

TEMPLATES = {
    "кавовий_апарат": {
        "product": "КавовийАпарат_Стандарт",
        "default_filename": "coffee_machine_config.txt",
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
    },
    "фехтувальне_екіпірування": {
        "product": "Fencing_Full_Set",
        "default_filename": "fencing_equipment_config.txt",
        "components": [
            "Рапіра",
            "Шпага",
            "Шабля",
            "Маска",
            "Куртка",
            "Штани",
            "Рукавиця",
            "Гетри",
            "ЕлектроКуртка_Рапіра",
            "ЕлектроКуртка_Шабля",
            "ЖилетПроводка_Рапіра"
        ],
        "dependencies": [
            "Рапіра CONFLICTS Шпага",
            "Рапіра CONFLICTS Шабля",
            "Шпага CONFLICTS Шабля",
            "Рапіра REQUIRES Маска",
            "Рапіра REQUIRES Куртка",
            "Рапіра REQUIRES Штани",
            "Рапіра REQUIRES Рукавиця",
            "Рапіра REQUIRES Гетри",
            "Шпага REQUIRES Маска",
            "Шпага REQUIRES Куртка",
            "Шпага REQUIRES Штани",
            "Шпага REQUIRES Рукавиця",
            "Шпага REQUIRES Гетри",
            "Шабля REQUIRES Маска",
            "Шабля REQUIRES Куртка",
            "Шабля REQUIRES Штани",
            "Шабля REQUIRES Рукавиця",
            "Шабля REQUIRES Гетри",
            "Рапіра REQUIRES ЕлектроКуртка_Рапіра",
            "Рапіра REQUIRES ЖилетПроводка_Рапіра",
            "Шпага CONFLICTS ЕлектроКуртка_Рапіра",
            "Шпага CONFLICTS ЕлектроКуртка_Шабля",
            "Шпага CONFLICTS ЖилетПроводка_Рапіра",
            "Шабля REQUIRES ЕлектроКуртка_Шабля",
            "Шабля CONFLICTS ЕлектроКуртка_Рапіра",
            "Шабля CONFLICTS ЖилетПроводка_Рапіра"
        ]
    },
    "пилосос": {
        "product": "Пилосос_Базовий",
        "default_filename": "vacuum_cleaner_config.txt",
        "components": [
            "HEPAФільтр",
            "ТурбоЩітка",
            "КонтейнерДляПилу",
            "НасадкаДляПідлоги",
            "Акумулятор",
        ],
        "dependencies": [
            "ТурбоЩітка REQUIRES Акумулятор",
            "HEPAФільтр REQUIRES КонтейнерДляПилу",
            "Акумулятор CONFLICTS НасадкаДляПідлоги"
        ]
    },
}


def create_config_file(template_name, output_filename=None):
    """Створює файл конфігурації на основі шаблону"""
    if template_name not in TEMPLATES:
        return False

    data = TEMPLATES[template_name]

    if output_filename is None:
        output_filename = data['default_filename']

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(f"{data['product']}\n")
        for comp in data['components']:
            f.write(f"{comp}\n")
        for dep in data['dependencies']:
            f.write(f"{dep}\n")

    print(f"Файл '{output_filename}' успішно створено!")
    print(f"Продукт: {data['product']}")
    print(f"Компонент: {len(data['components'])}")
    print(f"Залежностей: {len(data['dependencies'])}\n")
    return True


def create_custom_config():
    """Інтерактивне створення власної конфігурації"""
    print("СТВОРЕННЯ ВЛАСНОЇ КОНФІГУРАЦІЇ")

    product = input("Назва базового продукту: ").strip()
    while not product:
        print("Назва продукту не може бути порожньою!")
        product = input("Назва базового продукту: ").strip()

    print("Додавання компонент")
    print("(введіть порожній рядок для завершення)\n")
    components = []
    component_num = 1

    while True:
        comp = input(f"Компонента {component_num}: ").strip()
        if not comp:
            break
        if comp in components:
            print(f"Компонента '{comp}' вже додана!")
            continue
        components.append(comp)
        component_num += 1

    if not components:
        print("\nПотрібно додати хоча б одну компоненту!")
        return

    print(f"\nДодано компонент: {len(components)}")

    print("\nДодавання залежностей")
    print("Формат: A REQUIRES B або A CONFLICTS B")
    print("(введіть порожній рядок для завершення)\n")

    dependencies = []
    dep_num = 1

    while True:
        dep = input(f"Залежність {dep_num}: ").strip()
        if not dep:
            break

        if "REQUIRES" not in dep and "CONFLICTS" not in dep:
            print("Залежність має містити REQUIRES або CONFLICTS!")
            continue

        dependencies.append(dep)
        dep_num += 1

    print(f"Додано залежностей: {len(dependencies)}")

    safe_product_name = product.lower().replace(" ", "_").replace("-", "_")
    default_filename = f"{safe_product_name}_config.txt"

    custom_filename = input(f"\nІм'я файлу ({default_filename}): ").strip()
    if not custom_filename:
        custom_filename = default_filename

    with open(custom_filename, 'w', encoding='utf-8') as f:
        f.write(f"{product}\n")
        for comp in components:
            f.write(f"{comp}\n")
            for dep in dependencies:
                f.write(f"{dep}\n")

    print(f"Файл '{custom_filename}' успішно створено!")
    print(f"Продукт: {product}")
    print(f"Компонент: {len(components)}")
    print(f"Залежностей: {len(dependencies)}\n")


def show_templates():
    """Показує доступні шаблони з детальною інформацією"""
    print("ДОСТУПНІ ШАБЛОНИ")

    for i, (name, data) in enumerate(TEMPLATES.items(), 1):
        print(f"{i}. {name}")
        print(f"Продукт: {data['product']}")
        print(f"Компонент: {len(data['components'])}")
        print(f"Залежностей: {len(data['dependencies'])}")
        print(f"Файл: {data['default_filename']}")
        print()


def show_template_details(template_name):
    """Показує детальну інформацію про шаблон"""
    if template_name not in TEMPLATES:
        return

    data = TEMPLATES[template_name]
    print(f"ДЕТАЛІ ШАБЛОНУ: {template_name}")
    print(f"Продукт: {data['product']}\n")

    print("Компоненти:")
    for i, comp in enumerate(data['components'], 1):
        print(f"  {i}. {comp}")

    print("\nЗалежності:")
    for i, dep in enumerate(data['dependencies'], 1):
        print(f"  {i}. {dep}")
    print()


def get_template_choice():
    """Запитує користувача вибрати шаблон з перевіркою"""
    while True:
        template_choice = input("Введіть назву шаблону: ").strip()

        if template_choice in TEMPLATES:
            return template_choice

        print(f"Шаблон '{template_choice}' не знайдено!")
        print(f"Доступні шаблони: {', '.join(TEMPLATES.keys())}\n")

        retry = input("Спробувати ще раз? (так/ні): ").strip().lower()
        if retry != 'так':
            return None


def main():
    """Головна функція програми"""
    while True:
        print("ГЕНЕРАТОР КОНФІГУРАЦІЙ 2-SAT")
        print("Оберіть дію:")
        print("1 - Створити конфігурацію з шаблону")
        print("2 - Створити власну конфігурацію")
        print("3 - Переглянути деталі шаблону")
        choice = input("\nВаш вибір (1-3): ").strip()

        if choice == "1":
            show_templates()
            template_choice = get_template_choice()

            if template_choice:
                use_default = input("Використати дефолтну назву файлу? (так/ні): ").strip().lower()

                if use_default == 'так':
                    create_config_file(template_choice)
                else:
                    filename = input("Введіть назву файлу: ").strip()
                    if not filename:
                        filename = TEMPLATES[template_choice]['default_filename']
                    create_config_file(template_choice, filename)

        elif choice == "2":
            create_custom_config()

        elif choice == "3":
            show_templates()
            template_choice = get_template_choice()
            if template_choice:
                show_template_details(template_choice)
                input("\nНатисніть Enter для повернення в меню")
        else:
            print("Неправильний вибір\n")

if __name__ == "__main__":
    main()
