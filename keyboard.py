from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_inline_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("✍️ Тема по запросу", callback_data="menu_idea"),
        InlineKeyboardButton("🤖 Тема сгенерированная ИИ", callback_data="menu_uniq"),
        InlineKeyboardButton("💡 Помощь с темой", callback_data="menu_help"),
    )
    return kb


def get_uniq_inline_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_menu"),
        InlineKeyboardButton("🎲 Сгенерировать", callback_data="uniq_generate"),
        InlineKeyboardButton("⭐ Моё избранное", callback_data="show_favorites")
    )
    return kb


def get_uniq_result_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_uniq"),
        InlineKeyboardButton("🎲 Сгенерировать", callback_data="uniq_generate"),
        InlineKeyboardButton("⭐ Добавить в избранное", callback_data="add_favorite")
    )
    return kb


def get_uniq_result_saved_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_uniq"),
        InlineKeyboardButton("🎲 Сгенерировать", callback_data="uniq_generate")
    )
    return kb


def get_back_inline_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_menu"),
        InlineKeyboardButton("🔁 Ещё раз", callback_data="repeat")
    )
    return kb


def get_only_back_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_menu")
    )
    return kb


def get_favorites_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_uniq")
    )
    return kb


def get_favorites_with_delete_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("🗑️ Удалить последнюю добавленную тему", callback_data="delete_last_favorite"),
        InlineKeyboardButton("⬅️ Назад", callback_data="back_to_uniq")
    )
    return kb
