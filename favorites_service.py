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


def build_favorites_view(user_id, get_favorites, source="uniq"):
    favorites = get_favorites(user_id)

    if not favorites:
        back_callback = "back_to_menu" if source == "main" else "back_to_uniq"
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(InlineKeyboardButton("⬅️ Назад", callback_data=back_callback))
        return "⭐ У тебя пока нет избранных тем", kb

    return "⭐ Твои избранные темы:\n\nНажми на тему, чтобы открыть её полностью.", get_favorites_topics_keyboard(
        favorites, source)


def delete_last_favorite_and_build_view(user_id, delete_last_favorite, get_favorites, source="uniq"):
    deleted = delete_last_favorite(user_id)

    if not deleted:
        return None, None, False

    favorites = get_favorites(user_id)

    if not favorites:
        back_callback = "back_to_menu" if source == "main" else "back_to_uniq"
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(InlineKeyboardButton("⬅️ Назад", callback_data=back_callback))
        return "⭐ Последняя тема удалена.\n\nУ тебя больше нет избранных тем.", kb, True

    text = "⭐ Последняя тема удалена.\n\nНажми на тему, чтобы открыть её полностью."
    return text, get_favorites_topics_keyboard(favorites, source), True


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
