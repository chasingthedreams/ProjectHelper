# импорты
import os
import telebot
from dotenv import load_dotenv

from database import save_request, init_db, get_last_topics, add_favorite, get_favorites, delete_last_favorite
from keyboard import (get_main_inline_keyboard, get_uniq_inline_keyboard, get_back_inline_keyboard,
                      get_only_back_keyboard, get_uniq_result_keyboard, get_favorites_keyboard,
                      get_favorites_with_delete_keyboard, get_uniq_result_saved_keyboard)
from promts import system_prompt_uniq, system_prompt_help, system_prompt_idea, base_system_prompt
from ollama import ask_gemma

# инициализация
load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")
init_db()

# состояния и хранение
user_last_uniq_topic = {}
user_last_menu = {}
user_states = {}
user_active_message = {}


# ии/промт
def build_prompt(system_prompt, user_text):
    return (
            base_system_prompt
            + "\n\n"
            + system_prompt
            + "\n\nЗАПРОС ПОЛЬЗОВАТЕЛЯ:\n"
            + (user_text or "")
    )


def safe_gemma(prompt):
    try:
        response = ask_gemma(prompt)
        if not response or not response.strip():
            return "⚠️ *Не удалось получить ответ.*"
        return response.strip()
    except Exception as e:
        print("Ошибка Ollama:", e)
        return "❌ *ИИ временно недоступна.*"


# уи текст
def main_menu_text(user):
    name = user.first_name

    return (
        f"👋 *Привет, {name}, добро пожаловать в главное меню.*\n\n"
        "✨ Я помогаю с идеями проектов и анализом твоего проекта.\n\n"
        "📌 Что я умею:\n"
        "• 📝 придумать тему по запросу\n"
        "• 🎲 сгенерировать случайную идею\n"
        "• 🧠 помочь доработать тему\n\n"
        "👇 Выбирай действие:"
    )


def show_generation_message(chat_id, msg_id):
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=msg_id,
        text="⏳ *Генерация ответа...*"
    )


# обработчик старта
@bot.message_handler(commands=["start"])
def handle_start(message):
    sent = bot.send_message(
        message.chat.id,
        main_menu_text(message.from_user),
        reply_markup=get_main_inline_keyboard()
    )

    user_states[message.from_user.id] = None
    user_active_message[message.from_user.id] = sent.message_id


# обработчик нажатий инлайн кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    data = call.data

    if data != "add_favorite":
        bot.answer_callback_query(call.id)

    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id

    user_active_message[user_id] = msg_id

    # ================== кнопка назад ==================
    if data == "back_to_menu":
        user_states[user_id] = None

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text=main_menu_text(call.from_user),
            reply_markup=get_main_inline_keyboard()
        )

    elif data == "back_to_uniq":
        user_states[user_id] = "uniq"

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text=(
                "🎯 *Генерация уникальной темы проекта*\n\n"
                "Я подберу *простую и реализуемую тему*, "
                "которую можно без проблем разработать и защитить.\n\n"
                "⏳ После нажатия кнопки *«🎲 Сгенерировать»* "
                "ответ может появиться не сразу — обычно это занимает "
                "*10–20 секунд*.\n\n"
                "👇 Доступные действия:\n"
                "• 🎲 *Сгенерировать* — получить новую уникальную тему\n"
                "• ⬅️ *Назад* — вернуться в главное меню"
            ),
            reply_markup=get_uniq_inline_keyboard()
        )

    elif data == "delete_last_favorite":
        deleted = delete_last_favorite(user_id)

        if not deleted:
            bot.answer_callback_query(
                call.id,
                text="❗ В избранном нет тем",
                show_alert=True
            )
            return

        favorites = get_favorites(user_id)

        if not favorites:
            text = "⭐ *Последняя тема удалена.*\n\nУ тебя больше нет избранных тем."
            keyboard = get_favorites_keyboard()
        else:
            text = "⭐ *Последняя тема удалена.*\n\n" + "\n\n".join(
                f"{i + 1}. {t}" for i, t in enumerate(favorites)
            )
            keyboard = get_favorites_with_delete_keyboard()

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text=text,
            reply_markup=keyboard
        )

    # ================== кнопка еще раз ==================
    elif data == "repeat":
        last = user_last_menu.get(user_id)

        if last == "menu_idea":
            user_states[user_id] = "awaiting_idea"
            text = "📝 *Опиши, с чем должен быть связан проект* 👇"

        elif last == "menu_help":
            user_states[user_id] = "awaiting_help"
            text = "🧠 *Опиши тему или задай вопрос* 👇"

        else:
            return

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text=text,
            reply_markup=get_only_back_keyboard()
        )

    # ================== генерация уникальной темы ==================
    elif data == "menu_uniq":
        user_states[user_id] = "uniq"

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text=(
                "🎯 *Генерация уникальной темы проекта*\n\n"
                "Я подберу *простую и реализуемую тему*, "
                "которую можно без проблем разработать и защитить.\n\n"
                "⏳ После нажатия кнопки *«🎲 Сгенерировать»* "
                "ответ может появиться не сразу — обычно это занимает "
                "*10–20 секунд*.\n\n"
                "👇 Доступные действия:\n"
                "• 🎲 *Сгенерировать* — получить новую уникальную тему\n"
                "• ⬅️ *Назад* — вернуться в главное меню"
            ),
            reply_markup=get_uniq_inline_keyboard()
        )

    elif data == "uniq_generate":
        last_topics = get_last_topics(user_id, limit=15)
        rules_block = ""

        if last_topics:
            rules_block = (
                    "\n\nРАНЕЕ СГЕНЕРИРОВАННЫЕ ТЕМЫ:\n"
                    + "\n".join(f"- {t[:100]}" for t in last_topics)
            )

        show_generation_message(chat_id, msg_id)

        response = safe_gemma(
            build_prompt(system_prompt_uniq + rules_block, "")
        )

        user_last_uniq_topic[user_id] = response
        save_request(user_id, "uniq", "", response)

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text=response,
            reply_markup=get_uniq_result_keyboard()
        )

    elif data == "add_favorite":
        topic = user_last_uniq_topic.get(user_id)

        if not topic:
            bot.answer_callback_query(
                call.id,
                text="❗ Нет темы для добавления",
                show_alert=True
            )
            return

        add_favorite(user_id, topic)
        bot.answer_callback_query(
            call.id,
            text="⭐ Тема добавлена в избранное"
        )

        bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=msg_id,
            reply_markup=get_uniq_result_saved_keyboard()
        )

    elif data == "show_favorites":
        favorites = get_favorites(user_id)

        if not favorites:
            text = "⭐ *У тебя пока нет избранных тем*"
            keyboard = get_favorites_keyboard()
        else:
            text = "⭐ *Твои избранные темы:*\n\n" + "\n\n".join(f"{i + 1}. {t}" for i, t in enumerate(favorites))
            keyboard = get_favorites_with_delete_keyboard()

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text=text,
            reply_markup=keyboard
        )

    # ================== тема по запросу ==================
    elif data == "menu_idea":
        user_states[user_id] = "awaiting_idea"
        user_last_menu[user_id] = "menu_idea"

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text=(
                "📝 *Тема проекта по твоему запросу*\n\n"
                "Опиши, с чем должен быть связан проект: предмет, направление, "
                "интересующую область или примерную идею.\n\n"
                "⏳ После отправки сообщения ответ может появиться не сразу — "
                "обычно генерация занимает *10–20 секунд*.\n\n"
                "⬅️ *Назад* — вернуться в главное меню.\n\n"
                "👇 Напиши свой запрос:"
            ),
            reply_markup=get_only_back_keyboard()
        )

    # ================== помощь ==================
    elif data == "menu_help":
        user_states[user_id] = "awaiting_help"
        user_last_menu[user_id] = "menu_help"

        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text=(
                "🧠 *Помощь с темой проекта*\n\n"
                "Напиши тему проекта или задай вопрос — я помогу уточнить формулировку, "
                "улучшить идею или подсказать, как её доработать.\n\n"
                "⏳ Ответ формируется не мгновенно — "
                "обычно это занимает *10–20 секунд*.\n\n"
                "⬅️ *Назад* — вернуться в главное меню.\n\n"
                "👇 Опиши тему или задай вопрос:"
            ),
            reply_markup=get_only_back_keyboard()
        )


# обработчик текста
@bot.message_handler(content_types=["text"])
def handle_text(message):
    user_id = message.from_user.id
    state = user_states.get(user_id)
    msg_id = user_active_message.get(user_id)

    user_message_id = message.message_id

    if not msg_id:
        return

    if state == "awaiting_idea":
        show_generation_message(message.chat.id, msg_id)

        response = safe_gemma(
            build_prompt(system_prompt_idea, message.text)
        )
        save_request(user_id, "idea", message.text, response)

    elif state == "awaiting_help":
        show_generation_message(message.chat.id, msg_id)

        response = safe_gemma(
            build_prompt(system_prompt_help, message.text)
        )
        save_request(user_id, "help", message.text, response)

    else:
        return

    is_error = response.startswith("⚠️") or response.startswith("❌")
    keyboard = get_back_inline_keyboard()

    bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=msg_id,
        text=response,
        reply_markup=keyboard
    )

    try:
        bot.delete_message(message.chat.id, user_message_id)
    except:
        pass

    if not is_error:
        user_states[user_id] = None


# запуск бота
if __name__ == "__main__":
    print("Бот запущен")
    bot.polling(none_stop=True)
