from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboard import (
    get_help_result_keyboard,
    get_help_result_saved_keyboard,
    get_idea_result_keyboard,
    get_idea_result_saved_keyboard,
    get_smart_result_keyboard,
    get_smart_result_saved_keyboard,
    get_uniq_result_keyboard,
    get_uniq_result_saved_keyboard,
    get_favorites_topics_keyboard
)
from states import user_data, ensure_user_data

PAGE_SIZE = 5


def build_favorites_view(user_id, get_favorites, source="uniq"):
    ensure_user_data(user_id)
    favorites = get_favorites(user_id)

    if not favorites:
        back_callback = "back_to_menu" if source == "main" else "back_to_uniq"
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(InlineKeyboardButton("⬅️ Назад", callback_data=back_callback))
        return "⭐ У тебя пока нет избранных тем", kb

    total_pages = (len(favorites) + PAGE_SIZE - 1) // PAGE_SIZE
    page = user_data[user_id].get("favorites_page", 0)

    if page < 0:
        page = 0
    if page >= total_pages:
        page = total_pages - 1

    user_data[user_id]["favorites_page"] = page

    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    page_items = favorites[start:end]

    text = (
        "⭐ Твои избранные темы:\n\n"
        "Нажми на тему, чтобы открыть её полностью."
    )

    keyboard = get_favorites_topics_keyboard(
        page_items,
        page,
        total_pages,
        start_index=start,
        source=source
    )

    return text, keyboard


def delete_last_favorite_and_build_view(user_id, delete_last_favorite, get_favorites, source="uniq"):
    deleted = delete_last_favorite(user_id)

    if not deleted:
        return None, None, False

    ensure_user_data(user_id)
    favorites = get_favorites(user_id)

    if not favorites:
        user_data[user_id]["favorites_page"] = 0
        back_callback = "back_to_menu" if source == "main" else "back_to_uniq"
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(InlineKeyboardButton("⬅️ Назад", callback_data=back_callback))
        return "⭐ Последняя тема удалена.\n\nУ тебя больше нет избранных тем.", kb, True

    total_pages = (len(favorites) + PAGE_SIZE - 1) // PAGE_SIZE
    page = user_data[user_id].get("favorites_page", 0)

    if page >= total_pages:
        page = total_pages - 1
    if page < 0:
        page = 0

    user_data[user_id]["favorites_page"] = page

    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    page_items = favorites[start:end]

    text = "⭐ Последняя тема удалена.\n\nНажми на тему, чтобы открыть её полностью."
    keyboard = get_favorites_topics_keyboard(
        page_items,
        page,
        total_pages,
        start_index=start,
        source=source
    )

    return text, keyboard, True


def get_saved_result_keyboard_by_mode(mode):
    if mode == "smart":
        return get_smart_result_saved_keyboard()
    if mode == "idea":
        return get_idea_result_saved_keyboard()
    if mode == "help":
        return get_help_result_saved_keyboard()
    return get_uniq_result_saved_keyboard()


def get_result_keyboard_by_mode(mode):
    if mode == "smart":
        return get_smart_result_keyboard()
    if mode == "idea":
        return get_idea_result_keyboard()
    if mode == "help":
        return get_help_result_keyboard()
    return get_uniq_result_keyboard()