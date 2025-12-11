import streamlit as st
from sat_solver import solve_2sat_from_rules, find_feasible_configurations,read_config_from_file
from itertools import combinations

# Функції для перевірки можливості конфігурації (застарілі, але залишаємо для сумісності)
def check_feasibility(selected_features, requirements, conflicts):
    """Перевіряє, чи можлива обрана конфігурація"""
    # Перевірка вимог (REQUIRES)
    for feature, required in requirements:
        if feature in selected_features and required not in selected_features:
            return False, f"Помилка: {feature} вимагає {required}"

    # Перевірка конфліктів (CONFLICTS)
    for feature1, feature2 in conflicts:
        if feature1 in selected_features and feature2 in selected_features:
            return False, f"Конфлікт: {feature1} конфліктує з {feature2}"

    return True, "Конфігурація можлива!"

def check_feasibility_2sat(selected_features, requirements, conflicts, all_components):
    """Перевіряє можливість конфігурації за допомогою 2-SAT"""
    # Використовуємо 2-SAT для перевірки
    feasible, assignment, message = solve_2sat_from_rules(
        requirements, conflicts, all_components
    )

    if not feasible:
        return False, message

    # Додатково перевіряємо, чи вибрані компоненти відповідають призначенню
    for component in selected_features:
        if component not in assignment:
            continue
        if not assignment[component]:
            return False, f"Компонент {component} не може бути вибраним згідно з правилами"

    return True, "Конфігурація можлива за алгоритмом 2-SAT!"

def find_all_feasible_combinations(all_features, requirements, conflicts):
    """Знаходить всі можливі комбінації функцій з використанням 2-SAT"""
    feasible_combinations = []

    # Використовуємо 2-SAT для пошуку всіх можливих конфігурацій
    all_configs = find_feasible_configurations(requirements, conflicts, all_features)

    return all_configs

# Шаблони продуктів (без телефону)
PRODUCT_TEMPLATES = {
    "кавовий_апарат": {
        "name": "Кавовий Апарат Стандарт",
        "icon": "☕",
        "components": [
            "РезервуарМолока",
            "Тент",
            "КаналПромивки",
            "ТенМолока",
            "ВеликийРезервуарВоди",
            "ДодатковийТен"
        ],
        "requirements": [
            ("РезервуарМолока", "Тент"),
            ("РезервуарМолока", "КаналПромивки"),
            ("ТенМолока", "КаналПромивки")
        ],
        "conflicts": [("ВеликийРезервуарВоди", "ДодатковийТен")],
        "description": "Кавовий апарат з можливістю приготування капучіно",
        "component_descriptions": {
            "РезервуарМолока": "Резервуар для зберігання молока",
            "Тент": "Захисний тент для резервуара",
            "КаналПромивки": "Система промивки каналів",
            "ТенМолока": "Нагрівач молока",
            "ВеликийРезервуарВоди": "Збільшений резервуар для води",
            "ДодатковийТен": "Додатковий нагрівальний елемент"
        }
    },
    "пилосос": {
        "name": "Пилосос Базовий",
        "icon": "🌀",
        "components": [
            "HEPAФільтр",
            "ТурбоЩітка",
            "КонтейнерДляПилу",
            "НасадкаДляПідлоги",
            "Акумулятор"
        ],
        "requirements": [
            ("ТурбоЩітка", "Акумулятор"),
            ("HEPAФільтр", "КонтейнерДляПилу")
        ],
        "conflicts": [("Акумулятор", "НасадкаДляПідлоги")],
        "description": "Потужний пилосос з різними насадками",
        "component_descriptions": {
            "HEPAФільтр": "Високоефективний фільтр повітря",
            "ТурбоЩітка": "Турбіна для видалення волосся та шерсті",
            "КонтейнерДляПилу": "Ємність для збору пилу",
            "НасадкаДляПідлоги": "Спеціальна насадка для миття підлоги",
            "Акумулятор": "Акумуляторна батарея для автономної роботи"
        }
    },
    "фехтувальне_спорядження": {
        "name": "Фехтувальне Спорядження",
        "icon": "🤺",
        "components": [
            "Рапіра", "Шпага", "Шабля", "Маска", "Куртка",
            "Штани", "Рукавиця", "Гетри", "ЕлектроКуртка_Рапіра",
            "ЕлектроКуртка_Шабля", "ЖилетПроводка_Рапіра"
        ],
        "requirements": [
            ("Рапіра", "Маска"), ("Рапіра", "Куртка"), ("Рапіра", "Штани"),
            ("Рапіра", "Рукавиця"), ("Рапіра", "Гетри"),
            ("Шпага", "Маска"), ("Шпага", "Куртка"), ("Шпага", "Штани"),
            ("Шпага", "Рукавиця"), ("Шпага", "Гетри"),
            ("Шабля", "Маска"), ("Шабля", "Куртка"), ("Шабля", "Штани"),
            ("Шабля", "Рукавиця"), ("Шабля", "Гетри"),
            ("Рапіра", "ЕлектроКуртка_Рапіра"),
            ("Рапіра", "ЖилетПроводка_Рапіра"),
            ("Шабля", "ЕлектроКуртка_Шабля")
        ],
        "conflicts": [
            ("Рапіра", "Шпага"), ("Рапіра", "Шабля"), ("Шпага", "Шабля"),
            ("Шпага", "ЕлектроКуртка_Рапіра"),
            ("Шпага", "ЕлектроКуртка_Шабля"),
            ("Шпага", "ЖилетПроводка_Рапіра"),
            ("Шабля", "ЕлектроКуртка_Рапіра"),
            ("Шабля", "ЖилетПроводка_Рапіра")
        ],
        "description": "Повний комплект спорядження для фехтування",
        "component_descriptions": {
            "Рапіра": "Спортивна рапіра для тренувань",
            "Шпага": "Спортивна шпага для змагань",
            "Шабля": "Спортивна шабля",
            "Маска": "Захисна маска для обличчя",
            "Куртка": "Захисна куртка",
            "Штани": "Захисні штани",
            "Рукавиця": "Захисна рукавиця",
            "Гетри": "Захисні гетри",
            "ЕлектроКуртка_Рапіра": "Електрифікована куртка для рапіри",
            "ЕлектроКуртка_Шабля": "Електрифікована куртка для шаблі",
            "ЖилетПроводка_Рапіра": "Жилет з проводкою для рапіри"
        }
    }
}

# Налаштування сторінки
st.set_page_config(
    page_title="Конфігуратор техніки (2-SAT)",
    page_icon="⚙️",
    layout="wide"
)

# CSS стилі
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        margin-top: 10px;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .product-card {
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        margin: 10px 0;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        transition: all 0.3s;
        cursor: pointer;
    }
    .product-card:hover {
        border-color: #4CAF50;
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    .product-card.selected {
        border-color: #4CAF50;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
    }
    .success-box {
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 2px solid #155724;
        color: #155724;
        margin: 20px 0;
    }
    .error-box {
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 2px solid #721c24;
        color: #721c24;
        margin: 20px 0;
    }
    .component-chip {
        display: inline-block;
        padding: 8px 16px;
        margin: 5px;
        background-color: #e3f2fd;
        border-radius: 25px;
        font-weight: 500;
        transition: all 0.3s;
    }
    .component-chip.selected {
        background-color: #4CAF50;
        color: white;
    }
    .dependency-item {
        padding: 8px;
        margin: 4px 0;
        background-color: #f8f9fa;
        border-left: 4px solid #6c757d;
        border-radius: 4px;
    }
    .stats-card {
        padding: 15px;
        border-radius: 10px;
        background-color: white;
        border: 1px solid #ddd;
        margin: 10px 0;
        text-align: center;
    }
    .sat-info-box {
        padding: 15px;
        border-radius: 10px;
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 2px solid #1976d2;
        color: #0d47a1;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Ініціалізація стану сесії
if 'selected_device' not in st.session_state:
    st.session_state.selected_device = None
if 'selected_features' not in st.session_state:
    st.session_state.selected_features = []
if 'check_result' not in st.session_state:
    st.session_state.check_result = None
if 'use_sat' not in st.session_state:
    st.session_state.use_sat = True  # За замовчуванням використовуємо 2-SAT
if 'sat_assignment' not in st.session_state:
    st.session_state.sat_assignment = {}

# Заголовок додатку
st.title("⚙️ Конфігуратор техніки (2-SAT алгоритм)")
st.markdown("---")

# Інформація про алгоритм
with st.expander("ℹ️ Про алгоритм 2-SAT", expanded=False):
    st.markdown("""
    ### Алгоритм 2-SAT (2-satisfiability)

    **2-SAT** — це спеціальний випадок задачі SAT, де кожна диз'юнкція містить не більше двох літералів.

    **Як працює в нашому конфігураторі:**
    1. Кожна компонента представляється як булева змінна
    2. Правила перетворюються в логічні формули:
       - `A REQUIRES B` → `(¬A ∨ B)` (або A → B)
       - `A CONFLICTS B` → `(¬A ∨ ¬B)` (або A → ¬B та B → ¬A)
    3. Будується граф імплікацій
    4. Знаходяться компоненти сильної зв'язності (алгоритм Тар'яна)
    5. Перевіряється наявність суперечностей (x та ¬x в одній компоненті)
    6. Якщо суперечностей немає, знаходиться відповідне призначення змінних

    **Переваги:**
    - Ефективний алгоритм (O(N+M), де N - кількість компонент, M - кількість правил)
    - Може знаходити всі можливі конфігурації
    - Обробляє складні залежності між компонентами
    """)

# Вибір пристрою
st.header("1. Виберіть тип продукту")
# Додаємо завантажувач файлів поруч з картками
##########
col_upload, _, _ = st.columns(3)
with col_upload:
    uploaded_file = st.file_uploader(
        "📤 Або завантажте файл",
        type=['txt'],
        help="Формат: компоненти по одному на рядок, або A REQUIRES B, або A CONFLICTS B",
        key="file_uploader"
    )

# Обробка завантаженого файлу
if uploaded_file is not None:
    try:
        custom_product = read_config_from_file(uploaded_file.read())

        if custom_product:
            # Зберігаємо у сесії
            st.session_state.uploaded_product = custom_product

            # Показуємо інформацію
            st.success(f"✅ Файл '{uploaded_file.name}' завантажено!")

            # Кнопка для використання
            if st.button(f"🎯 Використовувати кастомний продукт ({len(custom_product['components'])} компонентів)",
                        type="primary", use_container_width=True):
                PRODUCT_TEMPLATES["custom_uploaded"] = custom_product
                st.session_state.selected_device = "custom_uploaded"
                st.session_state.selected_features = []
                st.rerun()
    except Exception as e:
        st.error(f"❌ {str(e)}")
##########
# Показуємо всі доступні продукти у вигляді карток
product_keys = list(PRODUCT_TEMPLATES.keys())
cols = st.columns(3)

for idx, product_key in enumerate(product_keys):
    with cols[idx]:
        template = PRODUCT_TEMPLATES[product_key]

        # Визначаємо стиль картки
        card_class = "product-card"
        if st.session_state.selected_device == product_key:
            card_class += " selected"

        st.markdown(f"""
        <div class="{card_class}" onclick="this.nextElementSibling.click()">
            <div style="font-size: 2em; text-align: center;">{template['icon']}</div>
            <h3 style="text-align: center; margin: 10px 0;">{template['name']}</h3>
            <p style="text-align: center; font-size: 0.9em; color: #666;">
                {len(template['components'])} компонентів
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Обрати {template['name']}", key=f"btn_{product_key}"):
            st.session_state.selected_device = product_key
            st.session_state.selected_features = []
            st.session_state.check_result = None
            st.session_state.sat_assignment = {}
            st.rerun()

st.markdown("---")

# Якщо пристрій вибрано
if st.session_state.selected_device:
    # Визначаємо шаблон
    if st.session_state.selected_device == "custom_uploaded":
        template = st.session_state.uploaded_product
        product_name = f"{template['name']} (з файлу)"
    else:
        template = PRODUCT_TEMPLATES[st.session_state.selected_device]
        product_name = template['name']
    # template = PRODUCT_TEMPLATES[st.session_state.selected_device]

    # Заголовок з обраним продуктом
    col_title, col_change, col_algo = st.columns([3, 1, 1])
    with col_title:
        st.header(f"{template['icon']} Конфігурація: {template['name']}")
    with col_change:
        if st.button("🔄 Змінити продукт", type="secondary"):
            st.session_state.selected_device = None
            st.session_state.selected_features = []
            st.session_state.check_result = None
            st.session_state.sat_assignment = {}
            st.rerun()
    with col_algo:
        # Перемикач алгоритму
        st.session_state.use_sat = st.toggle("Використовувати 2-SAT", value=st.session_state.use_sat)

    # Опис продукту
    st.info(f"**Опис:** {template['description']}")

    # Інформація про алгоритм
    if st.session_state.use_sat:
        st.markdown("""
        <div class="sat-info-box">
            <strong>🔬 Використовується алгоритм 2-SAT</strong><br>
            Перевірка конфігурації за допомогою графу імплікацій та алгоритму Тар'яна
        </div>
        """, unsafe_allow_html=True)

    # Вибір компонентів
    st.subheader("2. Оберіть бажані компоненти:")

    # Групуємо компоненти по 3 в рядок
    components = template['components']
    component_descriptions = template.get('component_descriptions', {})

    # Створюємо чекбокси для вибору компонентів
    selected_features = []

    # Відображаємо компоненти в сітці
    for i in range(0, len(components), 3):
        cols = st.columns(3)
        row_components = components[i:i+3]

        for j, component in enumerate(row_components):
            with cols[j]:
                # Отримуємо опис компонента
                description = component_descriptions.get(component, "Опис недоступний")

                # Створюємо чекбокс з підказкою
                if st.checkbox(
                    f"**{component}**",
                    value=component in st.session_state.selected_features,
                    key=f"check_{component}",
                    help=description
                ):
                    if component not in selected_features:
                        selected_features.append(component)
                else:
                    if component in selected_features:
                        selected_features.remove(component)

    # Оновлюємо стан
    st.session_state.selected_features = selected_features

    # Статистика вибору
    st.markdown("---")
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

    with col_stat1:
        st.metric("Обрано", f"{len(selected_features)}/{len(components)}")

    with col_stat2:
        percent = (len(selected_features) / len(components) * 100) if components else 0
        st.metric("Відсоток", f"{percent:.1f}%")

    with col_stat3:
        requirements_count = len(template['requirements'])
        st.metric("Вимог", requirements_count)

    with col_stat4:
        conflicts_count = len(template['conflicts'])
        st.metric("Конфліктів", conflicts_count)

    # Кнопка перевірки конфігурації
    st.markdown("---")
    if st.button("🔍 Перевірити можливість конфігурації", type="primary", use_container_width=True):
        if not selected_features:
            st.error("⚠️ Будь ласка, оберіть хоча б одну компоненту!")
        else:
            if st.session_state.use_sat:
                # Використовуємо 2-SAT алгоритм
                feasible, assignment, message = solve_2sat_from_rules(
                    template['requirements'],
                    template['conflicts'],
                    components
                )

                # Перевіряємо конкретний вибір користувача
                user_feasible = True
                user_message = "Конфігурація можлива!"

                if feasible:
                    # Перевіряємо, чи відповідає вибір користувача призначенню
                    for component in selected_features:
                        if component in assignment and not assignment[component]:
                            user_feasible = False
                            user_message = f"Компонент '{component}' не може бути вибраним згідно з правилами"
                            break

                    # Додаткова перевірка вимог та конфліктів
                    if user_feasible:
                        for a, b in template['requirements']:
                            if a in selected_features and b not in selected_features:
                                user_feasible = False
                                user_message = f"Помилка: {a} вимагає {b}"
                                break

                        if user_feasible:
                            for a, b in template['conflicts']:
                                if a in selected_features and b in selected_features:
                                    user_feasible = False
                                    user_message = f"Конфлікт: {a} конфліктує з {b}"
                                    break
                else:
                    user_feasible = False
                    user_message = message

                st.session_state.check_result = {
                    'feasible': user_feasible,
                    'message': user_message,
                    'selected': selected_features.copy()
                }
                st.session_state.sat_assignment = assignment

            else:
                # Використовуємо старий алгоритм
                feasible, message = check_feasibility(
                    selected_features,
                    template['requirements'],
                    template['conflicts']
                )

                # Зберігаємо результат
                st.session_state.check_result = {
                    'feasible': feasible,
                    'message': message,
                    'selected': selected_features.copy()
                }
                st.session_state.sat_assignment = {}

    # Показуємо результат перевірки
    if st.session_state.check_result:
        st.markdown("---")
        result = st.session_state.check_result

        if result['feasible']:
            st.markdown(f"""
            <div class="success-box">
                <h3>✅ Конфігурація можлива!</h3>
                <p><strong>Обрано компонентів:</strong> {len(result['selected'])}</p>
                <p>{result['message']}</p>
                <p><strong>Алгоритм:</strong> {'2-SAT' if st.session_state.use_sat else 'Базова перевірка'}</p>
            </div>
            """, unsafe_allow_html=True)

            # Показуємо призначення 2-SAT (якщо доступно)
            if st.session_state.use_sat and st.session_state.sat_assignment:
                with st.expander("📊 Призначення 2-SAT", expanded=False):
                    st.write("**Статус компонентів за алгоритмом 2-SAT:**")

                    col_ass1, col_ass2 = st.columns(2)
                    true_components = [c for c, v in st.session_state.sat_assignment.items() if v]
                    false_components = [c for c, v in st.session_state.sat_assignment.items() if not v]

                    with col_ass1:
                        st.success("**Можуть бути активними:**")
                        for comp in true_components:
                            status = "✅ Обрано" if comp in selected_features else "○ Доступно"
                            st.write(f"- {comp} ({status})")

                    with col_ass2:
                        st.error("**Не можуть бути активними:**")
                        for comp in false_components:
                            st.write(f"- {comp}")

            # Показати всі можливі комбінації
            with st.expander("🔮 Показати всі можливі комбінації", expanded=False):
                if st.session_state.use_sat:
                    st.info("**Пошук всіх можливих комбінацій через 2-SAT...**")

                    # Для демонстрації показуємо тільки комбінації до 50
                    all_combinations = find_feasible_configurations(
                        template['requirements'],
                        template['conflicts'],
                        components
                    )

                    st.write(f"**Всього можливих комбінацій:** {len(all_combinations)}")

                    if len(all_combinations) > 0:
                        # Групуємо комбінації за кількістю компонентів
                        combos_by_size = {}
                        for combo in all_combinations:
                            size = len(combo)
                            if size not in combos_by_size:
                                combos_by_size[size] = []
                            combos_by_size[size].append(combo)

                        for size in sorted(combos_by_size.keys()):
                            with st.expander(f"Комбінації з {size} компонент(ами) ({len(combos_by_size[size])})"):
                                for i, combo in enumerate(combos_by_size[size][:20], 1):
                                    st.write(f"{i}. {', '.join(combo)}")

                                if len(combos_by_size[size]) > 20:
                                    st.write(f"... та ще {len(combos_by_size[size]) - 20} комбінацій")
                    else:
                        st.write("Не знайдено жодної можливої комбінації")
                else:
                    st.warning("Для перегляду всіх комбінацій увімкніть 2-SAT алгоритм")

        else:
            st.markdown(f"""
            <div class="error-box">
                <h3>❌ Конфігурація неможлива!</h3>
                <p><strong>Обрано компонентів:</strong> {len(result['selected'])}</p>
                <p>{result['message']}</p>
                <p><strong>Алгоритм:</strong> {'2-SAT' if st.session_state.use_sat else 'Базова перевірка'}</p>
            </div>
            """, unsafe_allow_html=True)

            # Детальний аналіз проблем
            with st.expander("🔍 Аналіз проблем", expanded=True):
                # Знаходимо конфлікти
                conflicts_found = []
                for conf in template['conflicts']:
                    if conf[0] in result['selected'] and conf[1] in result['selected']:
                        conflicts_found.append(f"**{conf[0]}** конфліктує з **{conf[1]}**")

                if conflicts_found:
                    st.write("### Конфлікти знайдено:")
                    for cf in conflicts_found:
                        st.write(f"⚡ {cf}")

                # Знаходимо незадоволені вимоги
                missing_reqs = []
                for req in template['requirements']:
                    if req[0] in result['selected'] and req[1] not in result['selected']:
                        missing_reqs.append(f"**{req[0]}** потребує **{req[1]}**")

                if missing_reqs:
                    st.write("### Відсутні необхідні компоненти:")
                    for mr in missing_reqs:
                        st.write(f"📌 {mr}")

                # Поради щодо виправлення
                if conflicts_found or missing_reqs:
                    st.write("### 💡 Поради щодо виправлення:")
                    advice = []
                    if conflicts_found:
                        advice.append("**Видаліть одну з конфліктуючих компонент**")
                    if missing_reqs:
                        advice.append("**Додайте відсутні необхідні компоненти**")
                        advice.append("**Або видаліть компоненти, що їх потребують**")

                    for i, adv in enumerate(advice, 1):
                        st.write(f"{i}. {adv}")

    # Правила конфігурації
    st.markdown("---")
    st.header("📋 Правила конфігурації")

    # Відображаємо правила для обраного продукту
    col_rules1, col_rules2 = st.columns(2)

    with col_rules1:
        if template['requirements']:
            st.subheader("Вимоги (REQUIRES):")
            for req in template['requirements']:
                st.markdown(f'<div class="dependency-item">📌 {req[0]} → {req[1]}</div>',
                          unsafe_allow_html=True)
        else:
            st.info("Немає вимог")

    with col_rules2:
        if template['conflicts']:
            st.subheader("Конфлікти (CONFLICTS):")
            for conf in template['conflicts']:
                st.markdown(f'<div class="dependency-item">⚡ {conf[0]} × {conf[1]}</div>',
                          unsafe_allow_html=True)
        else:
            st.info("Немає конфліктів")

    # Приклади можливих конфігурацій
    with st.expander("📚 Приклади можливих конфігурацій", expanded=False):
        if st.session_state.selected_device == "кавовий_апарат":
            st.markdown("""
            ### ☕ Приклади для кавового апарату:
            - ✅ РезервуарМолока + Тент + КаналПромивки
            - ✅ ТенМолока + КаналПромивки
            - ✅ ВеликийРезервуарВоди
            - ❌ ВеликийРезервуарВоди + ДодатковийТен (конфлікт)
            - ❌ РезервуарМолока без Тента (потребує тент)
            """)
        elif st.session_state.selected_device == "пилосос":
            st.markdown("""
            ### 🌀 Приклади для пилососа:
            - ✅ HEPAФільтр + КонтейнерДляПилу
            - ✅ ТурбоЩітка + Акумулятор
            - ✅ НасадкаДляПідлоги
            - ❌ Акумулятор + НасадкаДляПідлоги (конфлікт)
            - ❌ ТурбоЩітка без Акумулятора (потребує акумулятор)
            """)
        elif st.session_state.selected_device == "фехтувальне_спорядження":
            st.markdown("""
            ### 🤺 Приклади для фехтувального спорядження:
            - ✅ Рапіра + Маска + Куртка + Штани + Рукавиця + Гетри + ЕлектроКуртка_Рапіра + ЖилетПроводка_Рапіра
            - ✅ Шпага + Маска + Куртка + Штани + Рукавиця + Гетри
            - ✅ Шабля + Маска + Куртка + Штани + Рукавиця + Гетри + ЕлектроКуртка_Шабля
            - ❌ Рапіра + Шпага (конфлікт)
            - ❌ Рапіра без Маски (потребує маску)
            """)

else:
    # Екран вибору пристрою (якщо ще нічого не обрано)
    st.info("👆 **Будь ласка, оберіть тип продукту зверху**")

    # Детальна інформація про всі продукти
    st.markdown("---")
    st.header("ℹ️ Про доступні продукти")

    cols = st.columns(3)

    for idx, product_key in enumerate(product_keys):
        with cols[idx]:
            template = PRODUCT_TEMPLATES[product_key]

            st.markdown(f"""
            <div class="stats-card">
                <div style="font-size: 1.5em;">{template['icon']}</div>
                <h4>{template['name']}</h4>
                <p style="font-size: 0.9em; color: #666;">{template['description']}</p>
                <p><strong>Компонентів:</strong> {len(template['components'])}</p>
                <p><strong>Вимог:</strong> {len(template['requirements'])}</p>
                <p><strong>Конфліктів:</strong> {len(template['conflicts'])}</p>
            </div>
            """, unsafe_allow_html=True)

# Футер
st.markdown("---")
st.caption("© 2024 Конфігуратор техніки | Використовує алгоритм 2-SAT для перевірки конфігурацій")

# Бічна панель
with st.sidebar:
    st.title("⚙️ Налаштування")

    st.subheader("Поточний стан")
    if st.session_state.selected_device:
        ####
        if st.session_state.selected_device == "custom_uploaded":
            if st.button("🗑 Видалити завантажений шаблон", type="secondary"):
                if "custom_uploaded" in PRODUCT_TEMPLATES:
                    del PRODUCT_TEMPLATES["custom_uploaded"]
                if 'uploaded_product' in st.session_state:
                    del st.session_state.uploaded_product
                st.session_state.selected_device = None
                st.session_state.selected_features = []
                st.rerun()
        else:
        ####
            st.success(f"**Продукт:** {PRODUCT_TEMPLATES[st.session_state.selected_device]['name']}")
            st.info(f"**Обрано компонент:** {len(st.session_state.selected_features)}")
            st.info(f"**Алгоритм:** {'2-SAT' if st.session_state.use_sat else 'Базова перевірка'}")
        ####
        if st.session_state.check_result:
            if st.session_state.check_result['feasible']:
                st.success("✅ Конфігурація можлива")
            else:
                st.error("❌ Конфігурація неможлива")
    else:
        st.info("Продукт не обрано")

    st.markdown("---")

    st.subheader("Керування")
    if st.button("🔄 Скинути всі вибори", type="secondary"):
        st.session_state.selected_device = None
        st.session_state.selected_features = []
        st.session_state.check_result = None
        st.session_state.sat_assignment = {}
        st.rerun()

    if st.button("📋 Експортувати конфігурацію",
                 disabled=not st.session_state.selected_device or
                         not st.session_state.selected_features):
        if st.session_state.selected_device and st.session_state.selected_features:
            config_text = f"# Конфігурація: {PRODUCT_TEMPLATES[st.session_state.selected_device]['name']}\n\n"
            config_text += f"# Алгоритм перевірки: {'2-SAT' if st.session_state.use_sat else 'Базова перевірка'}\n\n"
            config_text += "## Обрані компоненти:\n"
            for comp in st.session_state.selected_features:
                config_text += f"- {comp}\n"

            config_text += "\n## Залежності:\n"
            for req in PRODUCT_TEMPLATES[st.session_state.selected_device]['requirements']:
                if req[0] in st.session_state.selected_features and req[1] in st.session_state.selected_features:
                    config_text += f"{req[0]} REQUIRES {req[1]}\n"

            for conf in PRODUCT_TEMPLATES[st.session_state.selected_device]['conflicts']:
                if conf[0] in st.session_state.selected_features and conf[1] in st.session_state.selected_features:
                    config_text += f"{conf[0]} CONFLICTS {conf[1]}\n"

            st.download_button(
                label="💾 Завантажити конфігурацію",
                data=config_text,
                file_name=f"{st.session_state.selected_device}_config.txt",
                mime="text/plain"
            )

    st.markdown("---")

    st.subheader("Формат файлу")

    example = """Компонент1
Компонент2
Компонент3
Компонент1 REQUIRES Компонент2
Компонент1 CONFLICTS Компонент3"""

    st.download_button(
        "📥 Приклад файлу",
        example,
        "приклад_конфігурації.txt",
        "text/plain"
    )

    st.subheader("Про алгоритм 2-SAT")
    st.info("""
    **2-SAT алгоритм:**
    1. Перетворює правила у логічні формули
    2. Будує граф імплікацій
    3. Знаходить компоненти сильної зв'язності
    4. Перевіряє на суперечності
    5. Знаходить призначення змінних
    """)

    st.subheader("Допомога")
    st.info("""
    **Інструкція:**
    1. Оберіть тип продукту
    2. Виберіть бажані компоненти
    3. Оберіть алгоритм перевірки
    4. Натисніть "Перевірити"
    5. Перегляньте результат
    6. При необхідності скоригуйте вибір
    """)
