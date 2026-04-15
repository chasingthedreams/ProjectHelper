from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_inline_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("✍️ Подобрать тему", callback_data="menu_idea"),
        InlineKeyboardButton("🤖 Генерация темы", callback_data="menu_uniq"),
        InlineKeyboardButton("💡 Доработать тему", callback_data="menu_help"),
        InlineKeyboardButton("📚 Разделы проекта", callback_data="project_help_open"),
        InlineKeyboardButton("⭐ Избранное", callback_data="main_favorites")
    )
    return kb


def get_uniq_inline_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_uniq"),
        InlineKeyboardButton("🎲 Новая тема", callback_data="uniq_generate"),
        InlineKeyboardButton("⭐ Избранное", callback_data="show_favorites")
    )
    return kb


def get_uniq_result_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_uniq"),
        InlineKeyboardButton("🎲 Новая тема", callback_data="uniq_generate"),
        InlineKeyboardButton("⭐ В избранное", callback_data="add_favorite")
    )
    return kb


def get_uniq_result_saved_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_uniq"),
        InlineKeyboardButton("🎲 Новая тема", callback_data="uniq_generate")
    )
    return kb


def get_back_inline_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_menu"),
        InlineKeyboardButton("🔁 Ещё раз", callback_data="repeat")
    )
    return kb


def get_idea_result_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_menu"),
        InlineKeyboardButton("🔁 Ещё раз", callback_data="repeat"),
        InlineKeyboardButton("🧩 Упростить", callback_data="make_easier"),
        InlineKeyboardButton("✨ Улучшить", callback_data="make_more_interesting"),
        InlineKeyboardButton("⭐ В избранное", callback_data="add_favorite")
    )
    return kb


def get_idea_result_saved_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_menu"),
        InlineKeyboardButton("🔁 Ещё раз", callback_data="repeat"),
        InlineKeyboardButton("🧩 Упростить", callback_data="make_easier"),
        InlineKeyboardButton("✨ Улучшить", callback_data="make_more_interesting")
    )
    return kb


def get_help_result_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_menu"),
        InlineKeyboardButton("🔁 Ещё раз", callback_data="repeat"),
        InlineKeyboardButton("🧩 Упростить", callback_data="make_easier"),
        InlineKeyboardButton("✨ Улучшить", callback_data="make_more_interesting"),
        InlineKeyboardButton("⭐ В избранное", callback_data="add_favorite")
    )
    return kb


def get_help_result_saved_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_menu"),
        InlineKeyboardButton("🔁 Ещё раз", callback_data="repeat"),
        InlineKeyboardButton("🧩 Упростить", callback_data="make_easier"),
        InlineKeyboardButton("✨ Улучшить", callback_data="make_more_interesting")
    )
    return kb


def get_only_back_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_menu")
    )
    return kb


def get_direction_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🤖 ИИ / Боты", callback_data="dir_ai"),
        InlineKeyboardButton("🌱 Экология", callback_data="dir_eco"),
        InlineKeyboardButton("⚙️ Физика / Механика", callback_data="dir_phys"),
        InlineKeyboardButton("🧪 Химия / Биология", callback_data="dir_chem"),
        InlineKeyboardButton("🎨 Дизайн / Макеты", callback_data="dir_design"),
        InlineKeyboardButton("🎯 Свободная тема", callback_data="dir_free"),
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_uniq")
    )
    return kb


def get_project_type_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🛠 Практический", callback_data="type_practice"),
        InlineKeyboardButton("👀 Наблюдательный", callback_data="type_observe"),
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_uniq")
    )
    return kb


def get_duration_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📅 1 неделя", callback_data="time_1week"),
        InlineKeyboardButton("📆 2 недели", callback_data="time_2weeks"),
        InlineKeyboardButton("🗓 До 2 месяцев", callback_data="time_2months"),
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_uniq")
    )
    return kb


def get_visual_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("✅ Да", callback_data="visual_yes"),
        InlineKeyboardButton("❌ Нет", callback_data="visual_no"),
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_uniq")
    )
    return kb


def get_digital_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("✅ Да", callback_data="digital_yes"),
        InlineKeyboardButton("❌ Нет", callback_data="digital_no"),
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_uniq")
    )
    return kb


def get_smart_result_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🧩 Упростить", callback_data="make_easier"),
        InlineKeyboardButton("✨ Улучшить", callback_data="make_more_interesting"),
        InlineKeyboardButton("🔁 Другая тема", callback_data="smart_regenerate"),
        InlineKeyboardButton("⭐ В избранное", callback_data="add_favorite"),
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_uniq")
    )
    return kb


def get_smart_result_saved_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🧩 Упростить", callback_data="make_easier"),
        InlineKeyboardButton("✨ Улучшить", callback_data="make_more_interesting"),
        InlineKeyboardButton("🔁 Другая тема", callback_data="smart_regenerate"),
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_uniq")
    )
    return kb


def get_uniq_mode_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("⚡ Быстро", callback_data="uniq_mode_classic"),
        InlineKeyboardButton("🧩 По параметрам", callback_data="uniq_mode_smart"),
        InlineKeyboardButton("⭐ Избранное", callback_data="show_favorites"),
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_menu")
    )
    return kb


def get_topic_choice_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("✍️ Написать свою тему", callback_data="topic_write"),
        InlineKeyboardButton("⭐ Выбрать из избранных", callback_data="topic_favorites"),
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_menu")
    )
    return kb


def get_project_topic_back_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="project_help_open")
    )
    return kb


def get_project_sections_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📌 Актуальность", callback_data="project_relevance"),
        InlineKeyboardButton("🎯 Цель", callback_data="project_goal"),
        InlineKeyboardButton("📋 Задачи", callback_data="project_tasks"),
        InlineKeyboardButton("🔬 Объект и предмет", callback_data="project_object"),
        InlineKeyboardButton("💡 Гипотеза", callback_data="project_hypothesis"),
        InlineKeyboardButton("🛠 Методы", callback_data="project_methods"),
        InlineKeyboardButton("🗂 План", callback_data="project_plan"),
        InlineKeyboardButton("📄 Заключение", callback_data="project_conclusion"),
        InlineKeyboardButton("📚 Всё сразу", callback_data="project_all"),
        InlineKeyboardButton("⬅️ Назад", callback_data="project_help_open")
    )
    return kb


def get_project_favorites_keyboard(favorites):
    kb = InlineKeyboardMarkup(row_width=1)
    MAX_LEN = 40

    for i, topic in enumerate(favorites):
        title = topic
        if "Название проекта:" in topic:
            try:
                title = topic.split("Название проекта:")[1].strip()
                title = title.split("\n")[0].strip()
                title = title.replace("🔹", "").strip()
            except:
                pass

        title = title.replace("\n", " ").strip()

        if len(title) > MAX_LEN:
            title = title[:MAX_LEN] + "..."

        kb.add(
            InlineKeyboardButton(
                title,
                callback_data=f"project_fav_{i}"
            )
        )

    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="project_help_open")
    )
    return kb


def get_favorites_topics_keyboard(favorites, source="uniq"):
    kb = InlineKeyboardMarkup(row_width=1)
    MAX_LEN = 40

    for i, topic in enumerate(favorites):
        title = topic
        if "Название проекта:" in topic:
            try:
                title = topic.split("Название проекта:")[1].strip()
                title = title.split("\n")[0].strip()
                title = title.replace("🔹", "").strip()
            except:
                pass

        title = title.replace("\n", " ").strip()

        if len(title) > MAX_LEN:
            title = title[:MAX_LEN] + "..."

        if i == 0:
            button_text = f"🆕 {title}"
        else:
            button_text = title

        kb.add(
            InlineKeyboardButton(
                button_text,
                callback_data=f"fav_open_{i}"
            )
        )

    if source == "main":
        kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_menu"))
    else:
        kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="back_to_uniq"))

    return kb


def get_single_favorite_keyboard(index, source="uniq"):
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton(
            "🗑️ Удалить из избранного",
            callback_data=f"fav_delete_{index}"
        )
    )

    if source == "main":
        kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="main_favorites"))
    else:
        kb.add(InlineKeyboardButton("⬅️ Назад", callback_data="show_favorites"))

    return kb