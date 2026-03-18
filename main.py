# импорты
import os
import telebot
from dotenv import load_dotenv
from database import save_request, init_db, get_last_topics, add_favorite, get_favorites, delete_last_favorite
from keyboard import *
from texts import *
from states import *
from promts import system_prompt_uniq, system_prompt_help, system_prompt_idea, base_system_prompt
from utils import build_prompt, safe_gemma, show_generation_message
import telebot.apihelper as apihelper
import time
from session_data import *
from generation_service import (
    generate_smart_topic,
    regenerate_smart_topic,
    make_topic_easier,
    make_topic_more_interesting,
    generate_classic_topic
)
from favorites_service import (
    build_favorites_view,
    delete_last_favorite_and_build_view,
    get_saved_result_keyboard_by_mode
)

# инициализация
load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")
init_db()

apihelper.CONNECT_TIMEOUT = 30
apihelper.READ_TIMEOUT = 30


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

        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=main_menu_text(call.from_user),
                reply_markup=get_main_inline_keyboard()
            )
        except Exception as e:
            print("Ошибка back_to_menu:", e)


    elif data == "back_to_uniq":
        user_states[user_id] = None
        user_data[user_id] = {}
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=uniq_mode_text(),
                reply_markup=get_uniq_mode_keyboard()
            )
        except Exception as e:
            print("Ошибка back_to_uniq:", e)


    elif data == "delete_last_favorite":
        text, keyboard, deleted = delete_last_favorite_and_build_view(user_id, delete_last_favorite, get_favorites)
        if not deleted:
            bot.answer_callback_query(
                call.id,
                text="❗ В избранном нет тем",
                show_alert=True
            )
            return
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=text,
                reply_markup=keyboard
            )
        except Exception as e:
            print("Ошибка delete_favorite:", e)

# кнопка ещё раз
    elif data == "repeat":
        last = user_last_menu.get(user_id)

        if last == "menu_idea":
            user_states[user_id] = "awaiting_idea"
            text = repeat_idea_text()

        elif last == "menu_help":
            user_states[user_id] = "awaiting_help"
            text = repeat_help_text()

        else:
            return

        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=text,
                reply_markup=get_only_back_keyboard()
            )
        except Exception as e:
            print("Ошибка repeat:", e)

# генерация уникальной темы
    elif data == "menu_uniq":
        user_states[user_id] = None
        user_data[user_id] = {}

        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=uniq_mode_text(),
                reply_markup=get_uniq_mode_keyboard()
            )
        except Exception as e:
            print("Ошибка menu_uniq:", e)

    elif data == "uniq_mode_classic":
        user_states[user_id] = "uniq"

        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=uniq_classic_text(),
                reply_markup=get_uniq_inline_keyboard()
            )
        except Exception as e:
            print("Ошибка uniq_mode_classic:", e)

    elif data == "uniq_mode_smart":
        user_states[user_id] = STATE_SELECT_DIRECTION
        user_data[user_id] = {}

        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=uniq_smart_start_text(),
                reply_markup=get_direction_keyboard()
            )
        except Exception as e:
            print("Ошибка uniq_mode_smart:", e)


    elif data.startswith("dir_"):
        user_states[user_id] = save_direction(user_id, data)
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=uniq_step_project_type_text(),
                reply_markup=get_project_type_keyboard()
            )

        except Exception as e:

            print("Ошибка выбора направления:", e)


    elif data.startswith("type_"):
        user_states[user_id] = save_project_type(user_id, data)
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=uniq_step_duration_text(),
                reply_markup=get_duration_keyboard()
            )
        except Exception as e:
            print("Ошибка выбора типа проекта:", e)


    elif data.startswith("time_"):
        user_states[user_id] = save_duration(user_id, data)
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=uniq_step_visual_text(),
                reply_markup=get_visual_keyboard()
            )
        except Exception as e:
            print("Ошибка выбора сроков:", e)


    elif data.startswith("visual_"):
        user_states[user_id] = save_visual(user_id, data)
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=uniq_step_digital_text(),
                reply_markup=get_digital_keyboard()
            )
        except Exception as e:
            print("Ошибка выбора визуального результата:", e)



    elif data.startswith("digital_"):
        save_digital(user_id, data)
        show_generation_message(bot, chat_id, msg_id)
        response = generate_smart_topic(user_id, get_last_topics, build_prompt, base_system_prompt, system_prompt_uniq,
                                        build_smart_uniq_prompt, safe_gemma, save_request)
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=response,
                reply_markup=get_smart_result_keyboard()
            )
        except Exception as e:
            print("Ошибка smart generate:", e)
        if not response.startswith("⚠️") and not response.startswith("❌"):
            user_states[user_id] = None


    elif data == "smart_regenerate":
        show_generation_message(bot, chat_id, msg_id)
        response = regenerate_smart_topic(user_id, get_last_topics, build_prompt, base_system_prompt,
                                          system_prompt_uniq, build_smart_uniq_prompt, safe_gemma, save_request)
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=response,
                reply_markup=get_smart_result_keyboard()
            )
        except Exception as e:
            print("Ошибка smart_regenerate:", e)


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
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=response,
                reply_markup=get_smart_result_keyboard()
            )
        except Exception as e:
            print("Ошибка make_easier:", e)


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
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=response,
                reply_markup=get_smart_result_keyboard()
            )
        except Exception as e:
            print("Ошибка make_more_interesting:", e)


    elif data == "uniq_generate":
        show_generation_message(bot, chat_id, msg_id)
        response = generate_classic_topic(user_id, get_last_topics, build_prompt, base_system_prompt,
                                          system_prompt_uniq, safe_gemma, save_request)
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=response,
                reply_markup=get_uniq_result_keyboard()
            )
        except Exception as e:
            print("Ошибка uniq_generate:", e)

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

        try:
            mode = user_last_uniq_mode.get(user_id)
            keyboard = get_saved_result_keyboard_by_mode(mode)

            bot.edit_message_reply_markup(
                chat_id=chat_id,
                message_id=msg_id,
                reply_markup=keyboard
            )
        except Exception as e:
            print("Ошибка add_favorite:", e)


    elif data == "show_favorites":
        text, keyboard = build_favorites_view(user_id, get_favorites)
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=text,
                reply_markup=keyboard
            )
        except Exception as e:
            print("Ошибка show_favorites:", e)

# тема по запросу
    elif data == "menu_idea":
        user_states[user_id] = "awaiting_idea"
        user_last_menu[user_id] = "menu_idea"

        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=menu_idea_text(),
                reply_markup=get_only_back_keyboard()
            )
        except Exception as e:
            print("Ошибка menu_idea:", e)

# помощь
    elif data == "menu_help":
        user_states[user_id] = "awaiting_help"
        user_last_menu[user_id] = "menu_help"

        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=menu_help_text(),
                reply_markup=get_only_back_keyboard()
            )
        except Exception as e:
            print("Ошибка menu_help:", e)


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

    elif state == "awaiting_help":
        show_generation_message(bot, message.chat.id, msg_id)

        response = safe_gemma(
            build_prompt(base_system_prompt, system_prompt_help, message.text)
        )
        save_request(user_id, "help", message.text, response)

    else:
        return

    is_error = response.startswith("⚠️") or response.startswith("❌")
    keyboard = get_back_inline_keyboard()

    try:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=msg_id,
            text=response,
            reply_markup=keyboard
        )
    except Exception as e:
        print("Ошибка ответа:", e)

    try:
        bot.delete_message(message.chat.id, user_message_id)
    except:
        pass

    if not is_error:
        user_states[user_id] = None


# запуск бота
if __name__ == "__main__":
    print("Бот запущен")

    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=30)
        except Exception as e:
            print("Ошибка polling:", e)
            time.sleep(5)
