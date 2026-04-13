STATE_SELECT_DIRECTION = "select_direction"
STATE_PROJECT_TYPE = "project_type"
STATE_DURATION = "duration"
STATE_VISUAL = "visual"
STATE_DIGITAL = "digital"

user_data = {}

def ensure_user_data(user_id):
    if user_id not in user_data:
        user_data[user_id] = {}


def build_smart_uniq_prompt(user_id, get_last_topics, build_prompt, base_system_prompt, system_prompt_uniq):
    data = user_data.get(user_id, {})

    direction = data.get("direction", "Свободная тема")
    project_type = data.get("project_type", "Практический")
    duration = data.get("duration", "до 2 месяцев")
    visual = data.get("visual", "Да")
    digital = data.get("digital", "Нет")

    last_topics = get_last_topics(user_id, limit=30)
    rules_block = ""

    if last_topics:
        rules_block = (
            "\n\n⚠️ ПРАВИЛО ДЛЯ ГЕНЕРАЦИИ:\n"
            "• НЕ повторяй темы из списка ниже\n"
            "• Каждый новый проект должен быть принципиально другим\n"
            "\nЗАПРЕЩЁННЫЕ ПОВТОРЫ:\n"
            + "\n".join(f"{i + 1}. {t[:120]}" for i, t in enumerate(last_topics))
        )

    user_prompt = (
        f"Направление проекта: {direction}\n"
        f"Тип проекта: {project_type}\n"
        f"Срок выполнения: {duration}\n"
        f"Нужен визуальный результат: {visual}\n"
        f"Нужны цифровые элементы: {digital}\n\n"
        "Подбери одну тему проекта строго под эти условия.\n"
        "Тема должна быть понятной, живой, выполнимой для студента 1 курса.\n"
        "Практический результат должен быть наглядным и удобным для защиты."
    )

    return build_prompt(base_system_prompt, system_prompt_uniq + rules_block, user_prompt)


def save_direction(user_id, data):
    ensure_user_data(user_id)

    direction_map = {
        "dir_ai": "ИИ / Боты",
        "dir_eco": "Экология",
        "dir_phys": "Физика / Механика",
        "dir_chem": "Химия / Биология",
        "dir_design": "Дизайн / Макеты",
        "dir_free": "Свободная тема"
    }

    user_data[user_id]["direction"] = direction_map.get(data)
    return STATE_PROJECT_TYPE


def save_project_type(user_id, data):
    ensure_user_data(user_id)

    project_type_map = {
        "type_practice": "Практический",
        "type_observe": "Наблюдательный"
    }

    user_data[user_id]["project_type"] = project_type_map.get(data)
    return STATE_DURATION


def save_duration(user_id, data):
    ensure_user_data(user_id)

    duration_map = {
        "time_1week": "1 неделя",
        "time_2weeks": "2 недели",
        "time_2months": "до 2 месяцев"
    }

    user_data[user_id]["duration"] = duration_map.get(data)
    return STATE_VISUAL

def save_visual(user_id, data):
    ensure_user_data(user_id)

    visual_map = {
        "visual_yes": "Да",
        "visual_no": "Нет"
    }

    user_data[user_id]["visual"] = visual_map.get(data)
    return STATE_DIGITAL


def save_digital(user_id, data):
    ensure_user_data(user_id)

    digital_map = {
        "digital_yes": "Да",
        "digital_no": "Нет"
    }

    user_data[user_id]["digital"] = digital_map.get(data)


def build_easier_prompt(last_topic, build_prompt, base_system_prompt, system_prompt_uniq):
    user_prompt = (
        "Упрости эту тему проекта.\n"
        "Сделай её легче для реализации, но сохрани саму идею.\n"
        "Проект должен остаться интересным, понятным и выполнимым для студента 1 курса.\n"
        "Сохрани тот же формат ответа.\n\n"
        f"Исходная тема:\n{last_topic}"
    )
    return build_prompt(base_system_prompt, system_prompt_uniq, user_prompt)


def build_more_interesting_prompt(last_topic, build_prompt, base_system_prompt, system_prompt_uniq):
    user_prompt = (
        "Сделай эту тему проекта интереснее и живее.\n"
        "Добавь больше привлекательности для студента, но не делай проект сложным.\n"
        "Он должен остаться выполнимым за 1–2 месяца.\n"
        "Сохрани тот же формат ответа.\n\n"
        f"Исходная тема:\n{last_topic}"
    )
    return build_prompt(base_system_prompt, system_prompt_uniq, user_prompt)


def build_more_practical_prompt(last_topic, build_prompt, base_system_prompt, system_prompt_uniq):
    user_prompt = (
        "Сделай эту тему проекта практичнее.\n"
        "Добавь понятный результат, который можно реально показать на защите.\n"
        "Не усложняй проект и сохрани его выполнимым для студента 1 курса.\n"
        "Сохрани тот же формат ответа.\n\n"
        f"Исходная тема:\n{last_topic}"
    )
    return build_prompt(base_system_prompt, system_prompt_uniq, user_prompt)
