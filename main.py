# импорты
import os
import time
import telebot
import telebot.apihelper as apihelper
from dotenv import load_dotenv

# БД
from database import save_request, init_db, get_last_topics, add_favorite, get_favorites, delete_last_favorite, \
    is_favorite_exists

# Клавиатуры
from keyboard import get_main_inline_keyboard, get_uniq_inline_keyboard, get_uniq_result_keyboard, \
    get_back_inline_keyboard, get_only_back_keyboard, get_direction_keyboard, get_project_type_keyboard, \
    get_duration_keyboard, get_visual_keyboard, get_digital_keyboard, get_smart_result_keyboard, get_uniq_mode_keyboard, \
    get_topic_choice_keyboard, get_project_topic_back_keyboard, get_project_sections_keyboard, get_help_result_keyboard, \
    get_idea_result_keyboard, get_project_favorites_keyboard, get_single_favorite_keyboard

# Текста
from texts import main_menu_text, uniq_mode_text, uniq_classic_text, uniq_smart_start_text, uniq_step_project_type_text, \
    uniq_step_duration_text, uniq_step_visual_text, uniq_step_digital_text, menu_idea_text, menu_help_text, \
    project_help_text, project_help_write_topic, project_sections_text

# Состояния
from states import STATE_SELECT_DIRECTION, user_data, ensure_user_data, build_smart_uniq_prompt, save_direction, \
    save_project_type, save_duration, save_visual, save_digital, build_easier_prompt, build_more_interesting_prompt

from session_data import user_last_uniq_topic, user_last_menu, user_states, user_active_message, user_last_uniq_mode

# Промты
from prompts import system_prompt_uniq, system_prompt_help, system_prompt_idea, base_system_prompt, \
    build_project_section_prompt, system_prompt_project_sections, system_prompt_project_all

# Помощь
from utils import build_prompt, safe_gemma, show_generation_message

# Сервисы
from generation_service import generate_smart_topic, regenerate_smart_topic, make_topic_easier, \
    make_topic_more_interesting, generate_classic_topic
from favorites_service import build_favorites_view, delete_last_favorite_and_build_view, get_result_keyboard_by_mode, \
    get_saved_result_keyboard_by_mode

# инициализация
load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)
init_db()

apihelper.CONNECT_TIMEOUT = 30
apihelper.READ_TIMEOUT = 30


def generate_project_section(user_id, chat_id, msg_id, section_title, instruction, system_prompt, allow_list=False):
    if user_id not in user_data or "project_topic" not in user_data[user_id]:
        user_states[user_id] = "project_topic_choice"
        safe_edit_md(
            chat_id,
            msg_id,
            project_help_text(),
            get_topic_choice_keyboard()
        )
        return

    topic = user_data[user_id]["project_topic"]

    show_generation_message(bot, chat_id, msg_id)

    prompt = build_project_section_prompt(topic, section_title, instruction, allow_list)

    response = safe_gemma(
        build_prompt(base_system_prompt, system_prompt, prompt)
    )

    text = (
        f"📌 Тема проекта:\n{topic}\n\n"
        f"{section_title}\n\n{response}"
    )

    safe_edit_plain(
        chat_id,
        msg_id,
        text,
        get_project_sections_keyboard()
    )


def safe_edit_md(chat_id, msg_id, text, reply_markup=None):
    try:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    except Exception as e:
        if "message is not modified" in str(e):
            return
        print("Ошибка edit markdown:", e)


def safe_edit_plain(chat_id, msg_id, text, reply_markup=None):
    try:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=msg_id,
            text=text,
            reply_markup=reply_markup
        )
    except Exception as e:
        if "message is not modified" in str(e):
            return
        print("Ошибка edit plain:", e)


def safe_markup(chat_id, msg_id, reply_markup):
    try:
        bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=msg_id,
            reply_markup=reply_markup
        )
    except Exception as e:
        print("Ошибка markup:", e)


# обработчик старта
@bot.message_handler(commands=["start"])
def handle_start(message):
    ensure_user_data(message.from_user.id)
    sent = bot.send_message(
        message.chat.id,
        main_menu_text(message.from_user),
        reply_markup=get_main_inline_keyboard(),
        parse_mode="Markdown"
    )

    user_states[message.from_user.id] = None
    user_active_message[message.from_user.id] = sent.message_id


# обработчик нажатий инлайн кнопок
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    data = call.data

    try:
        bot.answer_callback_query(call.id)
    except:
        pass

    user_id = call.from_user.id
    chat_id = call.message.chat.id
    msg_id = call.message.message_id

    user_active_message[user_id] = msg_id

    # кнопка назад
    if data == "back_to_menu":
        user_states[user_id] = None
        user_data[user_id] = {}

        safe_edit_md(chat_id, msg_id, main_menu_text(call.from_user), get_main_inline_keyboard())


    elif data == "back_to_uniq":
        user_states[user_id] = None
        user_data[user_id] = {}

        safe_edit_md(chat_id, msg_id, uniq_mode_text(), get_uniq_mode_keyboard())



    elif data == "delete_last_favorite":
        source = user_data.get(user_id, {}).get("favorites_source", "uniq")
        text, keyboard, deleted = delete_last_favorite_and_build_view(user_id, delete_last_favorite, get_favorites,
                                                                      source)
        if not deleted:
            bot.answer_callback_query(
                call.id,
                text="❗ В избранном нет тем",
                show_alert=True
            )
            return

        safe_edit_plain(chat_id, msg_id, text, keyboard)

    # кнопка ещё раз
    elif data == "repeat":
        last = user_last_menu.get(user_id)

        if last == "menu_idea":
            user_states[user_id] = "awaiting_idea"
            text = menu_idea_text()

        elif last == "menu_help":
            user_states[user_id] = "awaiting_help"
            text = menu_help_text()

        else:
            return

        safe_edit_md(chat_id, msg_id, text, get_only_back_keyboard())

    # генерация уникальной темы
    elif data == "menu_uniq":
        user_states[user_id] = None
        user_data[user_id] = {}

        safe_edit_md(chat_id, msg_id, uniq_mode_text(), get_uniq_mode_keyboard())

    elif data == "uniq_mode_classic":
        user_states[user_id] = "uniq"

        safe_edit_md(chat_id, msg_id, uniq_classic_text(), get_uniq_inline_keyboard())

    elif data == "uniq_mode_smart":
        user_states[user_id] = STATE_SELECT_DIRECTION
        user_data[user_id] = {}

        safe_edit_md(chat_id, msg_id, uniq_smart_start_text(), get_direction_keyboard())


    elif data.startswith("dir_"):
        user_states[user_id] = save_direction(user_id, data)

        safe_edit_md(chat_id, msg_id, uniq_step_project_type_text(), get_project_type_keyboard())


    elif data.startswith("type_"):
        user_states[user_id] = save_project_type(user_id, data)

        safe_edit_md(chat_id, msg_id, uniq_step_duration_text(), get_duration_keyboard())


    elif data.startswith("time_"):
        user_states[user_id] = save_duration(user_id, data)

        safe_edit_md(chat_id, msg_id, uniq_step_visual_text(), get_visual_keyboard())


    elif data.startswith("visual_"):
        user_states[user_id] = save_visual(user_id, data)

        safe_edit_md(chat_id, msg_id, uniq_step_digital_text(), get_digital_keyboard())



    elif data.startswith("digital_"):
        save_digital(user_id, data)
        show_generation_message(bot, chat_id, msg_id)
        response = generate_smart_topic(user_id, get_last_topics, build_prompt, base_system_prompt, system_prompt_uniq,
                                        build_smart_uniq_prompt, safe_gemma, save_request)

        safe_edit_plain(chat_id, msg_id, response, get_smart_result_keyboard())

        if not response.startswith("⚠️") and not response.startswith("❌"):
            user_states[user_id] = None


    elif data == "smart_regenerate":
        show_generation_message(bot, chat_id, msg_id)
        response = regenerate_smart_topic(user_id, get_last_topics, build_prompt, base_system_prompt,
                                          system_prompt_uniq, build_smart_uniq_prompt, safe_gemma, save_request)

        safe_edit_plain(chat_id, msg_id, response, get_smart_result_keyboard())


    elif data == "make_easier":
        last_topic = user_last_uniq_topic.get(user_id)
        if not last_topic:
            bot.answer_callback_query(
                call.id,
                text="❗ Нет темы для изменения",
                show_alert=True
            )
            return
        show_generation_message(bot, chat_id, msg_id)
        response = make_topic_easier(user_id, build_prompt, base_system_prompt, system_prompt_uniq, build_easier_prompt,
                                     safe_gemma, save_request)
        keyboard = get_result_keyboard_by_mode(user_last_uniq_mode.get(user_id))

        safe_edit_plain(chat_id, msg_id, response, keyboard)


    elif data == "make_more_interesting":
        last_topic = user_last_uniq_topic.get(user_id)
        if not last_topic:
            bot.answer_callback_query(
                call.id,
                text="❗ Нет темы для изменения",
                show_alert=True
            )
            return
        show_generation_message(bot, chat_id, msg_id)
        response = make_topic_more_interesting(user_id, build_prompt, base_system_prompt, system_prompt_uniq,
                                               build_more_interesting_prompt, safe_gemma, save_request)
        keyboard = get_result_keyboard_by_mode(user_last_uniq_mode.get(user_id))

        safe_edit_plain(chat_id, msg_id, response, keyboard)


    elif data == "uniq_generate":
        show_generation_message(bot, chat_id, msg_id)
        response = generate_classic_topic(user_id, get_last_topics, build_prompt, base_system_prompt,
                                          system_prompt_uniq, safe_gemma, save_request)

        safe_edit_plain(chat_id, msg_id, response, get_uniq_result_keyboard())

    elif data == "add_favorite":
        topic = user_last_uniq_topic.get(user_id)

        if not topic:
            bot.answer_callback_query(
                call.id,
                text="❗ Нет темы для добавления",
                show_alert=True
            )
            return

        if is_favorite_exists(user_id, topic):
            bot.answer_callback_query(
                call.id,
                text="⭐ Эта тема уже в избранном",
                show_alert=True
            )
            return

        add_favorite(user_id, topic)
        bot.answer_callback_query(
            call.id,
            text="⭐ Сохранено в избранное",
            show_alert=True
        )

        mode = user_last_uniq_mode.get(user_id)
        keyboard = get_saved_result_keyboard_by_mode(mode)
        safe_markup(chat_id, msg_id, keyboard)



    elif data == "show_favorites":
        ensure_user_data(user_id)
        user_data[user_id]["favorites_source"] = "uniq"
        text, keyboard = build_favorites_view(user_id, get_favorites, "uniq")

        safe_edit_plain(chat_id, msg_id, text, keyboard)

    # тема по запросу
    elif data == "menu_idea":
        user_states[user_id] = "awaiting_idea"
        user_last_menu[user_id] = "menu_idea"

        safe_edit_md(chat_id, msg_id, menu_idea_text(), get_only_back_keyboard())

    # помощь
    elif data == "menu_help":
        user_states[user_id] = "awaiting_help"
        user_last_menu[user_id] = "menu_help"

        safe_edit_md(chat_id, msg_id, menu_help_text(), get_only_back_keyboard())

    # доработка проекта
    elif data == "project_help_open":
        user_states[user_id] = "project_topic_choice"
        user_last_menu[user_id] = "project_help_open"

        safe_edit_md(chat_id, msg_id, project_help_text(), get_topic_choice_keyboard())

    elif data == "topic_write":
        user_states[user_id] = "wait_project_topic"
        user_last_menu[user_id] = "topic_write"

        safe_edit_md(chat_id, msg_id, project_help_write_topic(), get_project_topic_back_keyboard())


    elif data == "project_relevance":
        section_title = "📍 Актуальность"
        instruction = (
            "Объясни, почему эта тема важна, какую проблему она решает "
            "и где может применяться."
        )

        generate_project_section(user_id, chat_id, msg_id, section_title, instruction, system_prompt_project_sections,
                                 allow_list=False)


    elif data == "project_goal":
        section_title = "🎯 Цель проекта"
        instruction = (
            "Сформулируй одну цель проекта. "
            "Начни со слов: Цель проекта — ..."
        )

        generate_project_section(user_id, chat_id, msg_id, section_title, instruction, system_prompt_project_sections,
                                 allow_list=False)

    elif data == "project_tasks":
        section_title = "📋 Задачи проекта"
        instruction = (
            "Напиши 4–5 задач проекта ТОЛЬКО нумерованным списком. "
            "Каждая задача должна начинаться с глагола: "
            "изучить, разработать, создать, проанализировать, исследовать."
        )

        generate_project_section(user_id, chat_id, msg_id, section_title, instruction, system_prompt_project_sections,
                                 allow_list=True)

    elif data == "project_object":
        section_title = "🔬 Объект и предмет исследования"
        instruction = (
            "Определи объект и предмет исследования для этого проекта."
        )

        generate_project_section(user_id, chat_id, msg_id, section_title, instruction, system_prompt_project_sections,
                                 allow_list=False)

    elif data == "project_hypothesis":
        section_title = "💡 Гипотеза"
        instruction = (
            "Сформулируй гипотезу проекта. "
            "Начни со слов: Если ..., то ..."
        )

        generate_project_section(user_id, chat_id, msg_id, section_title, instruction, system_prompt_project_sections,
                                 allow_list=False)

    elif data == "project_methods":
        section_title = "🛠 Методы исследования"
        instruction = (
            "Перечисли методы исследования, которые можно использовать в этом проекте."
        )

        generate_project_section(user_id, chat_id, msg_id, section_title, instruction, system_prompt_project_sections,
                                 allow_list=True)

    elif data == "project_plan":
        section_title = "🗂 План работы"
        instruction = (
            "Составь примерный план выполнения проекта по этапам."
        )

        generate_project_section(user_id, chat_id, msg_id, section_title, instruction, system_prompt_project_sections,
                                 allow_list=True)

    elif data == "project_conclusion":
        section_title = "📊 Заключение"
        instruction = (
            "Напиши заключение проекта с выводами."
        )

        generate_project_section(user_id, chat_id, msg_id, section_title, instruction, system_prompt_project_sections,
                                 allow_list=False)

    elif data == "project_all":
        section_title = "📚 Полное описание проекта"

        instruction = (
            "Напиши полный текст проекта со следующими разделами:\n"
            "Актуальность — текстом\n"
            "Цель — текстом\n"
            "Задачи — списком\n"
            "Объект и предмет — текстом\n"
            "Гипотеза — текстом\n"
            "Методы — списком\n"
            "План — списком\n"
            "Заключение — текстом"
        )

        generate_project_section(user_id, chat_id, msg_id, section_title, instruction, system_prompt_project_all,
                                 allow_list=False)

    elif data == "topic_favorites":
        ensure_user_data(user_id)
        user_data[user_id]["favorites_source"] = "project"

        favorites = get_favorites(user_id)

        if not favorites:
            safe_edit_md(
                chat_id,
                msg_id,
                "⭐ *Избранные темы*\n\n"
                "У тебя пока нет сохранённых тем.\n\n"
                "Сначала добавь тему в избранное, а потом здесь можно будет выбрать её для проекта.",
                get_project_topic_back_keyboard()
            )
            return

        safe_edit_md(
            chat_id,
            msg_id,
            "⭐ Выбери тему из избранных:",
            get_project_favorites_keyboard(favorites)
        )

    elif data.startswith("project_fav_"):
        favorites = get_favorites(user_id)

        try:
            index = int(data.replace("project_fav_", ""))
            topic = favorites[index]
        except (ValueError, IndexError):
            bot.answer_callback_query(
                call.id,
                text="❗ Не удалось выбрать тему",
                show_alert=True
            )
            return

        ensure_user_data(user_id)
        user_data[user_id]["project_topic"] = topic
        user_states[user_id] = "project_sections"

        safe_edit_md(
            chat_id,
            msg_id,
            project_sections_text(topic),
            get_project_sections_keyboard()
        )


    elif data == "main_favorites":
        ensure_user_data(user_id)
        user_data[user_id]["favorites_source"] = "main"
        text, keyboard = build_favorites_view(user_id, get_favorites, "main")

        safe_edit_plain(chat_id, msg_id, text, keyboard)

    elif data.startswith("fav_open_"):
        favorites = get_favorites(user_id)

        try:
            index = int(data.replace("fav_open_", ""))
            topic = favorites[index]
        except (ValueError, IndexError):
            bot.answer_callback_query(
                call.id,
                text="❗ Не удалось открыть тему",
                show_alert=True
            )
            return

        source = user_data.get(user_id, {}).get("favorites_source", "uniq")

        keyboard = get_single_favorite_keyboard(index, source)

        safe_edit_plain(
            chat_id,
            msg_id,
            topic,
            keyboard
        )

    elif data.startswith("fav_delete_"):
        from database import delete_favorite_by_index

        try:
            index = int(data.replace("fav_delete_", ""))
        except:
            bot.answer_callback_query(
                call.id,
                text="❗ Ошибка удаления",
                show_alert=True
            )
            return

        deleted = delete_favorite_by_index(user_id, index)

        if not deleted:
            bot.answer_callback_query(
                call.id,
                text="❗ Не удалось удалить",
                show_alert=True
            )
            return

        bot.answer_callback_query(
            call.id,
            text="🗑️ Тема удалена"
        )

        source = user_data.get(user_id, {}).get("favorites_source", "uniq")
        text, keyboard = build_favorites_view(user_id, get_favorites, source)

        safe_edit_plain(chat_id, msg_id, text, keyboard)


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
        show_generation_message(bot, message.chat.id, msg_id)

        response = safe_gemma(
            build_prompt(base_system_prompt, system_prompt_idea, message.text)
        )
        save_request(user_id, "idea", message.text, response)

        is_error = response.startswith("⚠️") or response.startswith("❌")
        if is_error:
            keyboard = get_back_inline_keyboard()
        else:
            user_last_uniq_topic[user_id] = response
            user_last_uniq_mode[user_id] = "idea"
            keyboard = get_idea_result_keyboard()

        safe_edit_plain(message.chat.id, msg_id, response, keyboard)

        try:
            bot.delete_message(message.chat.id, user_message_id)
        except:
            pass

        if not is_error:
            user_states[user_id] = None

    elif state == "awaiting_help":
        show_generation_message(bot, message.chat.id, msg_id)

        response = safe_gemma(
            build_prompt(base_system_prompt, system_prompt_help, message.text)
        )
        save_request(user_id, "help", message.text, response)

        is_error = response.startswith("⚠️") or response.startswith("❌")
        if is_error:
            keyboard = get_back_inline_keyboard()
        else:
            user_last_uniq_topic[user_id] = response
            user_last_uniq_mode[user_id] = "help"
            keyboard = get_help_result_keyboard()

        safe_edit_plain(message.chat.id, msg_id, response, keyboard)

        try:
            bot.delete_message(message.chat.id, user_message_id)
        except:
            pass

        if not is_error:
            user_states[user_id] = None

    elif state == "wait_project_topic":
        ensure_user_data(user_id)
        user_data[user_id]["project_topic"] = message.text
        topic = user_data[user_id]["project_topic"]

        text = project_sections_text(topic)

        safe_edit_plain(message.chat.id, msg_id, text, get_project_sections_keyboard())

        try:
            bot.delete_message(message.chat.id, user_message_id)
        except Exception as e:
            print("Ошибка удаления сообщения пользователя:", e)

        user_states[user_id] = "project_sections"

    else:
        return


# запуск бота
if __name__ == "__main__":
    print("Бот запущен")

    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=30)
        except Exception as e:
            print("Ошибка polling:", e)
            print("Перезапуск через 5 секунд...")
            time.sleep(5)
