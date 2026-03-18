from keyboard import (
    get_favorites_keyboard,
    get_favorites_with_delete_keyboard,
    get_smart_result_saved_keyboard,
    get_uniq_result_saved_keyboard
)


def build_favorites_view(user_id, get_favorites):
    favorites = get_favorites(user_id)

    if not favorites:
        return "⭐ *У тебя пока нет избранных тем*", get_favorites_keyboard()

    text = "⭐ *Твои избранные темы:*\n\n" + "\n\n".join(
        f"{i + 1}. {t}" for i, t in enumerate(favorites)
    )
    return text, get_favorites_with_delete_keyboard()


def delete_last_favorite_and_build_view(user_id, delete_last_favorite, get_favorites):
    deleted = delete_last_favorite(user_id)

    if not deleted:
        return None, None, False

    favorites = get_favorites(user_id)

    if not favorites:
        return "⭐ *Последняя тема удалена.*\n\nУ тебя больше нет избранных тем.", get_favorites_keyboard(), True

    text = "⭐ *Последняя тема удалена.*\n\n" + "\n\n".join(
        f"{i + 1}. {t}" for i, t in enumerate(favorites)
    )
    return text, get_favorites_with_delete_keyboard(), True


def get_saved_result_keyboard_by_mode(mode):
    if mode == "smart":
        return get_smart_result_saved_keyboard()
    return get_uniq_result_saved_keyboard()